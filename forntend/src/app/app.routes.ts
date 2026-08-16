import { Routes } from '@angular/router';

import { Portfolio } from './page/portfolio/portfolio';
import { ChatPage } from './page/chat-page/chat-page';

export const routes: Routes = [
  {
    path: '',
    component: Portfolio
  },

  {
    path: 'about',
    component: Portfolio
  },

  {
    path: 'projects',
    component: Portfolio
  },

  {
    path: 'skills',
    component: Portfolio
  },

  {
    path: 'chat',
    component: ChatPage
  },

  {
    path: '**',
    redirectTo: ''
  }
];