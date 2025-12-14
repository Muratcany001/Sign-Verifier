import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MainMenu } from './features/main-menuComponent/main-menu/main-menu';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MainMenu],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('signVerifierFrontend');
}
