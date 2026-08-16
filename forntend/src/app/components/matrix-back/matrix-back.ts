import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild, PLATFORM_ID, inject } from "@angular/core";
import { isPlatformBrowser } from "@angular/common";

@Component({
  selector: 'app-matrix-background',
  standalone: true,
  imports: [],
  templateUrl: './matrix-back.html',
  styleUrl: './matrix-back.css'
})
export class MatrixBackground
  implements AfterViewInit, OnDestroy {

  @ViewChild('matrixCanvas', { static: true })
  canvas!: ElementRef<HTMLCanvasElement>;

  private readonly isBrowser = isPlatformBrowser(inject(PLATFORM_ID));

  private ctx!: CanvasRenderingContext2D;

  private animationId = 0;

  private columns = 0;

  private drops: number[] = [];

  private readonly characters =
    '01ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}[]<>/\\$#@%&*+=-';


  ngAfterViewInit(): void {

    if (!this.isBrowser) {
      return;
    }

    this.initialize();

    this.animate();

    window.addEventListener(
      'resize',
      this.handleResize
    );
  }


  private initialize(): void {

    const canvas = this.canvas.nativeElement;

    const context = canvas.getContext('2d');

    if (!context) {
      return;
    }

    this.ctx = context;

    this.resizeCanvas();
  }


  private resizeCanvas = (): void => {

    const canvas = this.canvas.nativeElement;

    canvas.width = window.innerWidth;

    canvas.height = window.innerHeight;

    const fontSize = 14;

    this.columns =
      Math.floor(canvas.width / fontSize);

    this.drops =
      Array(this.columns)
        .fill(1)
        .map(() =>
          Math.random() * canvas.height / fontSize
        );
  };


  private animate = (): void => {

    const canvas = this.canvas.nativeElement;

    const fontSize = 14;

    /*
     * Transparent black creates the fading trail.
     */

    this.ctx.fillStyle =
      'rgba(0, 0, 0, 0.055)';

    this.ctx.fillRect(
      0,
      0,
      canvas.width,
      canvas.height
    );


    this.ctx.font =
      `${fontSize}px monospace`;


    for (let i = 0; i < this.columns; i++) {

      const character =
        this.characters[
          Math.floor(
            Math.random() *
            this.characters.length
          )
        ];


      const x =
        i * fontSize;

      const y =
        this.drops[i] * fontSize;


      this.ctx.fillStyle =
        'rgba(0, 255, 65, 0.18)';


      this.ctx.fillText(
        character,
        x,
        y
      );


      /*
       * Reset the column after it reaches
       * the bottom with a random delay.
       */

      if (
        y > canvas.height &&
        Math.random() > 0.975
      ) {

        this.drops[i] = 0;

      }


      this.drops[i]++;
    }


    this.animationId =
      requestAnimationFrame(
        this.animate
      );
  };


  ngOnDestroy(): void {

    if (!this.isBrowser) {
      return;
    }

    cancelAnimationFrame(
      this.animationId
    );

    window.removeEventListener(
      'resize',
      this.handleResize
    );
  }


  private handleResize = (): void => {

    this.resizeCanvas();

  };

}