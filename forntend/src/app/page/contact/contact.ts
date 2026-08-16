import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css'
})
export class Contact {

  contact = {
    name: '',
    email: '',
    message: ''
  };

  email = 'mohamedamine.saad@example.com';

  github = 'https://github.com/Mohamedaminesaadd';

  linkedin = 'https://www.linkedin.com/';

  location = 'Tunisia';


  sendMessage(): void {

    console.log('Contact form:', this.contact);

  }

}