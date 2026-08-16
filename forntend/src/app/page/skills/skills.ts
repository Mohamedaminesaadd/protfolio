import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA
} from '@angular/core';

import {
  SkillsCard,
  Skill
} from '../../shared/skills-card/skills-card';


@Component({
  selector: 'app-skills',
  standalone: true,

  imports: [
    SkillsCard
  ],

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  templateUrl: './skills.html',
  styleUrl: './skills.css',
})
export class Skills {


  /* =========================================
     MACHINE LEARNING
     ========================================= */

  mlSkills: Skill[] = [

     {
    name: 'Python',
    icon: 'simple-icons:python'
  },

  {
    name: 'PyTorch',
    icon: 'simple-icons:pytorch'
  },

  {
    name: 'TensorFlow',
    icon: 'simple-icons:tensorflow'
  },

  {
    name: 'Scikit-learn',
    icon: 'simple-icons:scikitlearn'
  },

  {
    name: 'OpenCV',
    icon: 'simple-icons:opencv'
  },

  {
    name: 'YOLO',
    icon: 'mdi:target'
  },

  {
    name: 'Pandas',
    icon: 'simple-icons:pandas'
  },

  {
    name: 'NumPy',
    icon: 'simple-icons:numpy'
  },

  {
    name: 'Computer Vision',
    icon: 'mdi:eye-outline'
  },

  {
    name: 'MLOps',
    icon: 'mdi:infinity'
  }

  ];


  /* =========================================
     FULL STACK
     ========================================= */

  fullStackSkills: Skill[] = [

    {
      name: 'FastAPI',
      icon: 'simple-icons:fastapi'
    },

    {
      name: 'React',
      icon: 'simple-icons:react'
    },

    {
      name: 'Angular',
      icon: 'simple-icons:angular'
    },

    {
      name: 'PostgreSQL',
      icon: 'simple-icons:postgresql'
    },

    {
      name: 'InfluxDB',
      icon: 'simple-icons:influxdb'
    },

    {
      name: 'Redis',
      icon: 'simple-icons:redis'
    },

    {
      name: 'Kafka',
      icon: 'simple-icons:apachekafka'
    },

    {
      name: 'WebSockets',
      icon: 'mdi:access-point-network'
    },

    {
      name: 'Docker',
      icon: 'simple-icons:docker'
    },

    {
      name: 'Kubernetes',
      icon: 'simple-icons:kubernetes'
    },

    {
      name: 'CI/CD',
      icon: 'mdi:infinity'
    }

  ];


  /* =========================================
     AI AGENTS & GENERATIVE AI
     ========================================= */

  aiAgentSkills: Skill[] = [

    {
      name: 'LangChain',
      icon: 'simple-icons:langchain'
    },

    {
      name: 'CrewAI',
      icon: 'mdi:robot-outline'
    },

    {
      name: 'RAG',
      icon: 'mdi:database-search'
    },

    {
      name: 'LLM',
      icon: 'mdi:brain'
    },

    {
      name: 'n8n',
      icon: 'simple-icons:n8n'
    },

    {
      name: 'AI Agents',
      icon: 'mdi:robot'
    }

  ];


  /* =========================================
     EMBEDDED LINUX
     ========================================= */

  embeddedSkills: Skill[] = [

    {
      name: 'Linux',
      icon: 'simple-icons:linux'
    },

    {
      name: 'U-Boot',
      icon: 'mdi:chip'
    },

    {
      name: 'Buildroot',
      icon: 'mdi:package-variant'
    },

    {
      name: 'Yocto Project',
      icon: 'mdi:linux'
    },

    {
      name: 'Device Tree',
      icon: 'mdi:file-tree'
    },

    {
      name: 'Cross Compilation',
      icon: 'mdi:tools'
    }

  ];


  /* =========================================
     SECURITY ENGINEERING
     ========================================= */

  securitySkills: Skill[] = [

    {
      name: 'Wazuh',
      icon: 'mdi:shield-check'
    },

    {
      name: 'Suricata',
      icon: 'mdi:shield-search'
    },

    {
      name: 'Zeek',
      icon: 'mdi:network'
    },

    {
      name: 'ELK Stack',
      icon: 'simple-icons:elastic'
    },

    {
      name: 'SIEM',
      icon: 'mdi:security'
    },

    {
      name: 'Threat Detection',
      icon: 'mdi:alert-shield'
    },

    {
      name: 'Log Analysis',
      icon: 'mdi:file-search'
    }

  ];


  /* =========================================
     ENGINEERING
     ========================================= */

  engineeringSkills: Skill[] = [

    {
      name: 'Git',
      icon: 'simple-icons:git'
    },

    {
      name: 'GitHub',
      icon: 'simple-icons:github'
    },

    {
      name: 'GitHub Actions',
      icon: 'simple-icons:githubactions'
    },

    {
      name: 'Jira',
      icon: 'simple-icons:jira'
    },

    {
      name: 'Docker',
      icon: 'simple-icons:docker'
    },

    {
      name: 'Agile / Scrum',
      icon: 'mdi:sync'
    },

    {
      name: 'CI/CD',
      icon: 'mdi:infinity'
    }

  ];

}