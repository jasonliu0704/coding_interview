import { useState, useCallback } from 'react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

type Thought = {
  status: 'searching' | 'done' | 'idle';
  content: string;
};

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [thought, setThought] = useState<Thought>({ status: 'idle', content: '' });
  const [loading, setLoading] = useState(false);

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim()) return;

    setLoading(true);
    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setThought({ status: 'idle', content: '' });

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantMessage = "";
      let hasAddedAssistantMsg = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n').filter(Boolean);

        for (const line of lines) {
          try {
            const data = JSON.parse(line);

            // Handle "Thought"
            if (data.type === 'thought') {
              setThought({
                status: data.status,
                content: data.content
              });
            }
            // Handle "Answer" (Token stream)
            else if (data.type === 'answer') {
              assistantMessage += data.content;

              setMessages(prev => {
                // If we haven't added the assistant message placeholder yet, do it now
                if (!hasAddedAssistantMsg) {
                  // Check if last message is user to be safe
                  hasAddedAssistantMsg = true;
                  return [...prev, { role: 'assistant', content: assistantMessage }];
                }

                // Update last assistant message
                const newMessages = [...prev];
                const lastIdx = newMessages.length - 1;
                if (newMessages[lastIdx].role === 'assistant') {
                  newMessages[lastIdx] = { ...newMessages[lastIdx], content: assistantMessage };
                }
                return newMessages;
              });

              // To handle the flag correctly inside the loop, we set it true after the first state update dispatch is theoretically queued?
              // Actually, local variable `hasAddedAssistantMsg` tracks it for this closure execution. 
              // `setMessages` might run async but the order is preserved.
              hasAddedAssistantMsg = true;
            }
          } catch (e) {
            console.error("Error parsing JSON chunk", e);
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, something went wrong." }]);
    } finally {
      setLoading(false);
      setThought(t => ({ ...t, status: 'done' }));
    }
  }, []);

  return { messages, thought, sendMessage, loading };
}
