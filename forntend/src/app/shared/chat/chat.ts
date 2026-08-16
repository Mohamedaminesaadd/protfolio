import {
  AfterViewChecked,
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild,
  inject
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

import { AIAgentService } from '../../services/ai-agent';

import {
  Message,
  ChatResponse
} from '../../models/chat.model';

import { MessageComponent } from '../message/message';


@Component({
  selector: 'app-chat',
  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    MessageComponent
  ],

  templateUrl: './chat.html',
  styleUrls: ['./chat.css']
})
export class Chat
  implements OnInit, OnDestroy, AfterViewChecked {


  // ============================================================
  // SERVICES
  // ============================================================

  private readonly aiAgent =
    inject(AIAgentService);

  private readonly cdr =
    inject(ChangeDetectorRef);


  // ============================================================
  // VIEW REFERENCES
  // ============================================================

  @ViewChild('chatMessages')
  chatMessages!: ElementRef<HTMLDivElement>;

  @ViewChild('messageInput')
  messageInput!: ElementRef<HTMLTextAreaElement>;


  // ============================================================
  // CHAT STATE
  // ============================================================

  messages: Message[] = [];

  newMessage = '';

  isTyping = false;

  error: string | null = null;


  // ============================================================
  // SUGGESTED QUESTIONS
  // ============================================================

  readonly suggestedQuestions = [
    "Tell me about Mohamed's AI projects",
    "What are his main technical skills?",
    "Tell me about his education",
    "What experience does he have?",
    "What technologies does he use?"
  ];


  // ============================================================
  // SUBSCRIPTIONS
  // ============================================================

  private subscriptions: Subscription[] = [];


  // ============================================================
  // SCROLL
  // ============================================================

  private shouldScroll = false;


  // ============================================================
  // CONVERSATION THREAD
  // ============================================================

  /**
   * Each browser keeps its own conversation thread.
   *
   * We DO NOT use a global/shared thread such as:
   *
   *     amine-session-001
   *
   * because that would make all users share the same
   * PostgreSQL LangGraph conversation.
   *
   * Instead:
   *
   *     Browser A → amine-UUID-A
   *     Browser B → amine-UUID-B
   *
   * The current thread is persisted in localStorage so
   * refreshing the page keeps the same conversation.
   */

  private readonly THREAD_STORAGE_KEY =
    'personal-ai-thread-id';

  threadId: string =
    this.getOrCreateThreadId();


  // ============================================================
  // INIT
  // ============================================================

  ngOnInit(): void {

    this.addWelcomeMessage();

  }


  // ============================================================
  // GET OR CREATE THREAD ID
  // ============================================================

  private getOrCreateThreadId(): string {

    /**
     * Check whether this browser already has a conversation.
     */

    const existingThreadId =
      localStorage.getItem(
        this.THREAD_STORAGE_KEY
      );

    if (
      existingThreadId &&
      existingThreadId.trim()
    ) {

      return existingThreadId;

    }


    /**
     * Create a completely new conversation.
     */

    const newThreadId =
      `amine-${crypto.randomUUID()}`;


    /**
     * Persist it for this browser.
     */

    localStorage.setItem(
      this.THREAD_STORAGE_KEY,
      newThreadId
    );


    return newThreadId;
  }


  // ============================================================
  // WELCOME MESSAGE
  // ============================================================

  private addWelcomeMessage(): void {

    const welcomeMessage: Message = {

      id: 'welcome',

      content:
        "👋 Hi! I'm Mohamed's personal AI assistant. " +
        "Ask me about his education, experience, skills, " +
        "projects, or GitHub repositories.",

      sender: 'ai',

      timestamp: new Date(),

      status: 'sent'

    };


    this.messages = [
      ...this.messages,
      welcomeMessage
    ];


    this.shouldScroll = true;

  }


  // ============================================================
  // AFTER VIEW CHECKED
  // ============================================================

  ngAfterViewChecked(): void {

    if (this.shouldScroll) {

      this.scrollToBottom();

      this.shouldScroll = false;

    }

  }


  // ============================================================
  // DESTROY
  // ============================================================

  ngOnDestroy(): void {

    this.subscriptions.forEach(
      subscription =>
        subscription.unsubscribe()
    );

    this.subscriptions = [];

  }


  // ============================================================
  // SEND MESSAGE
  // ============================================================

  sendMessage(): void {

    const trimmedMessage =
      this.newMessage.trim();


    // ----------------------------------------------------------
    // VALIDATION
    // ----------------------------------------------------------

    if (
      !trimmedMessage ||
      this.isTyping
    ) {

      return;

    }


    // ----------------------------------------------------------
    // CREATE USER MESSAGE
    // ----------------------------------------------------------

    const userMessage: Message = {

      id: `user-${Date.now()}`,

      content: trimmedMessage,

      sender: 'user',

      timestamp: new Date(),

      status: 'sending'

    };


    // ----------------------------------------------------------
    // ADD USER MESSAGE
    // ----------------------------------------------------------

    this.messages = [
      ...this.messages,
      userMessage
    ];


    // ----------------------------------------------------------
    // CLEAR INPUT
    // ----------------------------------------------------------

    this.newMessage = '';


    // ----------------------------------------------------------
    // UPDATE UI
    // ----------------------------------------------------------

    this.isTyping = true;

    this.error = null;

    this.shouldScroll = true;


    // ----------------------------------------------------------
    // DEBUG REQUEST
    // ----------------------------------------------------------

    console.log(
      '================================'
    );

    console.log(
      '🚀 AI AGENT REQUEST'
    );

    console.log(
      'Message:',
      trimmedMessage
    );

    console.log(
      'Thread ID:',
      this.threadId
    );

    console.log(
      '================================'
    );


    // ----------------------------------------------------------
    // SEND REQUEST TO FASTAPI
    // ----------------------------------------------------------

    const subscription =
      this.aiAgent
        .sendMessage(
          trimmedMessage,
          this.threadId
        )
        .subscribe({

          // ====================================================
          // SUCCESS
          // ====================================================

          next: (
            response: ChatResponse
          ) => {

            console.log(
              '================================'
            );

            console.log(
              '🤖 AI RESPONSE RECEIVED'
            );

            console.log(
              'Response:',
              response
            );

            console.log(
              'Answer:',
              response.answer
            );

            console.log(
              'Thread ID:',
              response.thread_id
            );

            console.log(
              '================================'
            );


            // --------------------------------------------------
            // VALIDATE RESPONSE
            // --------------------------------------------------

            if (
              !response ||
              typeof response.answer !== 'string'
            ) {

              console.error(
                'Invalid AI response:',
                response
              );

              userMessage.status =
                'error';

              this.isTyping = false;

              this.error =
                'The AI returned an invalid response.';

              this.cdr.detectChanges();

              return;

            }


            // --------------------------------------------------
            // USER MESSAGE SENT
            // --------------------------------------------------

            userMessage.status =
              'sent';


            // --------------------------------------------------
            // CREATE AI MESSAGE
            // --------------------------------------------------

            const aiMessage: Message = {

              id: `ai-${Date.now()}`,

              content: response.answer,

              sender: 'ai',

              timestamp: new Date(),

              status: 'sent'

            };


            // --------------------------------------------------
            // ADD AI MESSAGE
            // --------------------------------------------------

            this.messages = [
              ...this.messages,
              aiMessage
            ];


            // --------------------------------------------------
            // KEEP BACKEND THREAD ID
            // --------------------------------------------------

            if (
              response.thread_id &&
              response.thread_id.trim()
            ) {

              this.threadId =
                response.thread_id.trim();


              /**
               * Persist the backend thread ID.
               */

              localStorage.setItem(
                this.THREAD_STORAGE_KEY,
                this.threadId
              );

            }


            // --------------------------------------------------
            // RESET UI
            // --------------------------------------------------

            this.isTyping = false;

            this.error = null;

            this.shouldScroll = true;


            // --------------------------------------------------
            // FORCE UI UPDATE
            // --------------------------------------------------

            this.cdr.detectChanges();

          },


          // ====================================================
          // ERROR
          // ====================================================

          error: (error) => {

            console.error(
              '================================'
            );

            console.error(
              '❌ AI AGENT ERROR'
            );

            console.error(
              'Error:',
              error
            );

            console.error(
              '================================'
            );


            // --------------------------------------------------
            // UPDATE USER MESSAGE
            // --------------------------------------------------

            userMessage.status =
              'error';


            // --------------------------------------------------
            // RESET TYPING
            // --------------------------------------------------

            this.isTyping = false;


            // --------------------------------------------------
            // ERROR MESSAGE
            // --------------------------------------------------

            this.error =
              error?.error?.detail ||
              error?.message ||
              'Failed to get a response. Please try again.';


            this.shouldScroll = true;


            // --------------------------------------------------
            // FORCE UI UPDATE
            // --------------------------------------------------

            this.cdr.detectChanges();

          }

        });


    // ----------------------------------------------------------
    // STORE SUBSCRIPTION
    // ----------------------------------------------------------

    this.subscriptions.push(
      subscription
    );

  }


  // ============================================================
  // SEND SUGGESTED QUESTION
  // ============================================================

  sendSuggested(
    question: string
  ): void {

    this.newMessage =
      question;

    this.sendMessage();

  }


  // ============================================================
  // KEYBOARD
  // ============================================================

  handleKeyPress(
    event: KeyboardEvent
  ): void {

    if (
      event.key === 'Enter' &&
      !event.shiftKey
    ) {

      event.preventDefault();

      this.sendMessage();

    }

  }


  // ============================================================
  // TEXTAREA AUTO RESIZE
  // ============================================================

  autoResize(
    event: Event
  ): void {

    const textarea =
      event.target as HTMLTextAreaElement;


    textarea.style.height =
      'auto';


    const maxHeight =
      120;


    textarea.style.height =
      `${Math.min(
        textarea.scrollHeight,
        maxHeight
      )}px`;

  }


  // ============================================================
  // SCROLL TO BOTTOM
  // ============================================================

  private scrollToBottom(): void {

    if (!this.chatMessages) {

      return;

    }


    try {

      const element =
        this.chatMessages.nativeElement;


      element.scrollTop =
        element.scrollHeight;

    }

    catch (error) {

      console.warn(
        'Could not scroll chat:',
        error
      );

    }

  }


  // ============================================================
  // FOCUS INPUT
  // ============================================================

  focusInput(): void {

    this.messageInput
      ?.nativeElement
      ?.focus();

  }


  // ============================================================
  // NEW CONVERSATION
  // ============================================================

  newConversation(): void {

    // ----------------------------------------------------------
    // CREATE NEW UNIQUE THREAD
    // ----------------------------------------------------------

    this.threadId =
      `amine-${crypto.randomUUID()}`;


    // ----------------------------------------------------------
    // SAVE NEW THREAD
    // ----------------------------------------------------------

    localStorage.setItem(
      this.THREAD_STORAGE_KEY,
      this.threadId
    );


    // ----------------------------------------------------------
    // CLEAR MESSAGES
    // ----------------------------------------------------------

    this.messages = [];


    // ----------------------------------------------------------
    // RESET STATE
    // ----------------------------------------------------------

    this.error = null;

    this.isTyping = false;

    this.newMessage = '';


    // ----------------------------------------------------------
    // WELCOME MESSAGE
    // ----------------------------------------------------------

    this.addWelcomeMessage();


    // ----------------------------------------------------------
    // FOCUS INPUT
    // ----------------------------------------------------------

    setTimeout(() => {

      this.focusInput();

    });

  }

}