import { Component } from '@angular/core';

import { Home } from '../home/home';
import { About } from '../about/about';
import { Projects } from '../projects/projects';
import { Skills } from '../skills/skills';
import { Contact } from '../contact/contact';


@Component({
  selector: 'app-portfolio',

  standalone: true,

  imports: [
    Home,
    About,
    Projects,
    Skills,
    Contact
  ],

  templateUrl: './portfolio.html',

  styleUrl: './portfolio.css'
})
export class Portfolio {

}