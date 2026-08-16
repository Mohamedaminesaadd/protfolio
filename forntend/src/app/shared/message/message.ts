import {
  Component,
  Input
} from '@angular/core';

import { CommonModule } from '@angular/common';

import { Message } from '../../models/chat.model';


@Component({
  selector: 'app-message',
  standalone: true,

  imports: [
    CommonModule
  ],

  templateUrl: './message.html',
  styleUrls: ['./message.css']
})
export class MessageComponent {

  @Input()
  message!: Message;

}