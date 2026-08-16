import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  ChatRequest,
  ChatResponse
} from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class AIAgentService {

  private readonly http = inject(HttpClient);

  private readonly apiUrl =
    'http://localhost:8080/api/chat';

  sendMessage(
    message: string,
    threadId: string
  ): Observable<ChatResponse> {

    const request: ChatRequest = {
      message: message,
      thread_id: threadId
    };

    return this.http.post<ChatResponse>(
      this.apiUrl,
      request
    );
  }
}