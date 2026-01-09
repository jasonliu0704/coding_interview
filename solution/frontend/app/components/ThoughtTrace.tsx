'use client';

import { motion } from 'framer-motion';

type ThoughtProps = {
  status: 'searching' | 'done' | 'idle';
  content: string;
};

export default function ThoughtTrace({ status, content }: ThoughtProps) {
  if (status === 'idle' || !content) return null;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0 }}
      className="thought-trace"
    >
      {status === 'searching' && <div className="spinner" />}
      <span>{content}</span>
    </motion.div>
  );
}
