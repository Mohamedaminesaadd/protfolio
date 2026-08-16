import { Component, OnDestroy, OnInit, ChangeDetectorRef } from "@angular/core";

@Component({
  selector: "app-terminal",
  standalone: true,
  templateUrl: "./terminal.html",
  styleUrl: "./terminal.css"
})
export class Terminal implements OnInit, OnDestroy {

  name = "";
  role = "";
  passion = "";

  private readonly nameText = "Mohamed Amine Saad";
  private readonly roleText = "AI / Machine Learning Engineer";
  private readonly passionText = "Building intelligent systems";

  private animationFrame: number | null = null;
  private isDestroyed = false;
  private isTyping = false;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    // Start after a small delay
    setTimeout(() => {
      if (!this.isDestroyed) {
        this.startTypingSequence();
      }
    }, 500);
  }

  private startTypingSequence(): void {
    if (this.isTyping || this.isDestroyed) return;
    this.isTyping = true;

    this.typeTextWithRAF(this.nameText, "name", 30, () => {
      this.typeTextWithRAF(this.roleText, "role", 25, () => {
        this.typeTextWithRAF(this.passionText, "passion", 20, () => {
          this.isTyping = false;
        });
      });
    });
  }

  private typeTextWithRAF(
    text: string,
    property: "name" | "role" | "passion",
    speed: number,
    onComplete?: () => void
  ): void {
    // Cancel any existing animation
    if (this.animationFrame !== null) {
      cancelAnimationFrame(this.animationFrame);
      this.animationFrame = null;
    }

    // Reset the property
    this[property] = "";
    let index = 0;
    let lastTimestamp = 0;

    const typeNext = (timestamp: number) => {
      if (this.isDestroyed) return;

      if (lastTimestamp === 0) {
        lastTimestamp = timestamp;
      }

      // Control speed
      if (timestamp - lastTimestamp >= speed) {
        if (index < text.length) {
          this[property] = text.slice(0, index + 1);
          index++;
          lastTimestamp = timestamp;
          
          // Force change detection
          this.cdr.detectChanges();
        }
      }

      if (index < text.length) {
        this.animationFrame = requestAnimationFrame(typeNext);
      } else if (onComplete) {
        setTimeout(() => {
          if (!this.isDestroyed) {
            onComplete();
            this.cdr.detectChanges();
          }
        }, 150);
      }
    };

    this.animationFrame = requestAnimationFrame(typeNext);
  }

  ngOnDestroy(): void {
    this.isDestroyed = true;
    this.isTyping = false;
    
    if (this.animationFrame !== null) {
      cancelAnimationFrame(this.animationFrame);
      this.animationFrame = null;
    }
  }
}