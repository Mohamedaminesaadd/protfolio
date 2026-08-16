export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  status: 'sending' | 'sent' | 'error';
}

export interface ChatState {
  messages: Message[];
  isTyping: boolean;
  error: string | null;
}

export interface ChatRequest {
  message: string;
  thread_id: string;
}

export interface ChatResponse {
  answer: string;
  thread_id: string;
}