import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-code-editor',
  standalone: true,
  templateUrl: './editor.html',
  styleUrl: './editor.css'
})
export class Editor {

 @Input() developer = {
  name: 'Mohamed Amine Saad',
  role: 'AI Engineer & Software Engineer',
  education: 'Computer Engineering Student at ENIS',
  focus: 'Edge AI, Embedded Systems, Software Engineering & Intelligent Systems',
  location: 'Tunisia',
  passion: 'Building intelligent systems, AI agents, robotics and open-source technology'
};

}