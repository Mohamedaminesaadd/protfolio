import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { ProjectCart } from '../../shared/project-cart/project-cart';


export interface Project {
  fileName: string;
  fileIcon: string;
  code: string;
  tags: string[];
  liveUrl?: string;
  codeUrl?: string;
}


@Component({
  selector: 'app-projects',
  standalone: true,

  imports: [
    CommonModule,
    ProjectCart
  ],

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  templateUrl: './projects.html',
  styleUrl: './projects.css'
})
export class Projects {


  projects: Project[] = [

    /* =========================================
       HPIS
       ========================================= */

    {
      fileName: 'hpis-platform.py',

      fileIcon: 'mdi:heart-pulse',

      tags: [
        'ESP32',
        'FastAPI',
        'XGBoost',
        'ECG',
        'HRV',
        'InfluxDB',
        'Docker'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/HIPS',

      code: `
<span class="keyword">class</span> <span class="variable">HPIS</span>:
  <span class="comment"># Human Performance Intelligence System</span>

  sensors = [
    <span class="string">"ECG"</span>,
    <span class="string">"HRV"</span>,
    <span class="string">"SpO2"</span>,
    <span class="string">"Activity"</span>
  ]

  model = <span class="string">"XGBoost"</span>

  <span class="keyword">def</span> <span class="variable">analyze</span>(self, data):
      <span class="keyword">return</span> stress_prediction(data)
`
    },


    /* =========================================
       AI FITNESS COACH
       ========================================= */

    {
      fileName: 'ai-fitness-coach.py',

      fileIcon: 'logos:python',

      tags: [
        'Python',
        'PyTorch',
        'OpenCV',
        'MediaPipe',
        'Computer Vision'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/AI-Fitness-Coach-Setup-Dependencies',

      code: `
<span class="keyword">class</span> <span class="variable">FitnessCoach</span>:

  pose = <span class="variable">MediaPipe</span>()

  <span class="keyword">def</span> <span class="variable">analyze_exercise</span>(self, frame):

      landmarks = self.pose.detect(frame)

      <span class="keyword">return</span> posture_analysis(
          landmarks
      )

  <span class="comment"># Squat / Push-up / Leg Raise</span>
`
    },


    /* =========================================
       PHOTOVOLTAIC PLATFORM
       ========================================= */

    {
      fileName: 'photovoltaic-platform.ts',

      fileIcon: 'logos:angular',

      tags: [
        'Angular',
        'FastAPI',
        'PostgreSQL',
        'Docker',
        'REST API'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/platefome-de-gestion-de-travaill-dans-les-project-photopholtiaque',

      code: `
<span class="keyword">interface</span> <span class="variable">SolarProject</span> {

  id: <span class="keyword">number</span>;

  name: <span class="keyword">string</span>;

  status: <span class="keyword">string</span>;

  capacity: <span class="keyword">number</span>;
}


<span class="keyword">const</span> <span class="variable">projects</span> =
  solarService.getProjects();
`
    },


    /* =========================================
       BIG DATA TWITTER
       ========================================= */

    {
      fileName: 'twitter-analysis.py',

      fileIcon: 'logos:hadoop',

      tags: [
        'Hadoop',
        'Spark',
        'Hive',
        'Flask',
        'Angular'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/Big-Data-Twitter-Analysis-System-using-Hadoop',

      code: `
<span class="keyword">class</span> <span class="variable">TwitterPipeline</span>:

  <span class="comment"># Distributed sentiment analysis</span>

  hadoop = <span class="string">"HDFS"</span>

  spark = <span class="string">"Spark"</span>

  hive = <span class="string">"Hive"</span>

  <span class="keyword">def</span> <span class="variable">process</span>(self, tweets):

      data = self.clean(tweets)

      <span class="keyword">return</span> sentiment_analysis(data)
`
    },


    /* =========================================
       INVOICE CLASSIFICATION AI
       ========================================= */

    {
      fileName: 'invoice-ai.py',

      fileIcon: 'logos:pytorch',

      tags: [
        'PyTorch',
        'OCR',
        'OpenCV',
        'Machine Learning'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/facture_data',

      code: `
<span class="keyword">class</span> <span class="variable">InvoiceAI</span>:

  <span class="comment"># Intelligent document processing</span>

  ocr = <span class="string">"Tesseract"</span>

  model = <span class="string">"Donut / LayoutLM"</span>

  <span class="keyword">def</span> <span class="variable">extract</span>(self, document):

      text = self.ocr.extract(document)

      <span class="keyword">return</span> self.model.predict(text)
`
    },


    /* =========================================
       PYTORCH LEARNING
       ========================================= */

    {
      fileName: 'pytorch-learning.py',

      fileIcon: 'logos:pytorch',

      tags: [
        'PyTorch',
        'Deep Learning',
        'Neural Networks'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/PyTorch-Learning-Notebook',

      code: `
<span class="keyword">class</span> <span class="variable">NeuralNetwork</span>:

  <span class="keyword">def</span> <span class="variable">forward</span>(self, x):

      x = self.layer1(x)

      x = self.activation(x)

      <span class="keyword">return</span> self.layer2(x)
`
    },


    /* =========================================
       LLM FROM SCRATCH
       ========================================= */

    {
      fileName: 'llm-from-scratch.py',

      fileIcon: 'mdi:brain',

      tags: [
        'Python',
        'Transformers',
        'PyTorch',
        'LLM'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/LLm-from-scratch',

      code: `
<span class="keyword">class</span> <span class="variable">MiniGPT</span>:

  tokenizer = <span class="variable">Tokenizer</span>()

  model = <span class="variable">Transformer</span>()

  <span class="keyword">def</span> <span class="variable">generate</span>(self, prompt):

      tokens = self.tokenizer.encode(prompt)

      <span class="keyword">return</span> self.model.generate(tokens)
`
    },


    /* =========================================
       AGENT LAB
       ========================================= */

    {
      fileName: 'agent-lab.py',

      fileIcon: 'mdi:robot',

      tags: [
        'Python',
        'LangGraph',
        'AI Agents',
        'RAG'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/agent_lab',

      code: `
<span class="keyword">class</span> <span class="variable">Agent</span>:

  tools = []

  memory = []

  <span class="keyword">def</span> <span class="variable">run</span>(self, query):

      plan = self.reason(query)

      <span class="keyword">return</span> self.execute(plan)
`
    },


    /* =========================================
       AGENT LANGCHAIN
       ========================================= */

    {
      fileName: 'agent-langchain.py',

      fileIcon: 'mdi:robot-outline',

      tags: [
        'LangChain',
        'LangGraph',
        'RAG',
        'LLM'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/agent_langchain',

      code: `
<span class="keyword">def</span> <span class="variable">create_agent</span>():

  llm = <span class="variable">ChatModel</span>()

  tools = [
      github_tool,
      rag_tool
  ]

  agent = build_agent(
      llm,
      tools
  )

  <span class="keyword">return</span> agent
`
    },


    /* =========================================
       WEBSOCKET FROM SCRATCH
       ========================================= */

    {
      fileName: 'websocket-server.py',

      fileIcon: 'mdi:access-point-network',

      tags: [
        'Python',
        'WebSocket',
        'Real-Time',
        'Backend'
      ],

      liveUrl: '#',

      codeUrl:
        'https://github.com/Mohamedaminesaadd/web-socket-from-scratch',

      code: `
<span class="keyword">class</span> <span class="variable">WebSocketServer</span>:

  clients = []

  <span class="keyword">async def</span> <span class="variable">broadcast</span>(
      self,
      message
  ):

      <span class="keyword">for</span> client <span class="keyword">in</span> self.clients:

          <span class="keyword">await</span> client.send(message)
`
    }

  ];

}