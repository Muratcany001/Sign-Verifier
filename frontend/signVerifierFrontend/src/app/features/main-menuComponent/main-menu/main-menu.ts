import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Route } from '@angular/router';
import { MainMenuService } from '../main-menu-service';

@Component({
  selector: 'app-main-menu',
  imports: [],
  templateUrl: './main-menu.html',
  styleUrl: './main-menu.css',
})
export class MainMenu {
  mainMenuForm! : FormGroup;
  errorMessage: string ='';
  isLoading: boolean = false;
  file1: File | null = null;
  file2: File | null = null;
  result : any = null;

  constructor(
    private mainService: MainMenuService,
    private formBuilder: FormBuilder,
    private route : Route,
    private router : ActivatedRoute,
    private fb: FormBuilder
  ){}
  onFileSelected(event:any, fileNo:number){
    const file = event.target.files[0];
    if (fileNo ===1) this.file1 = file;
    else this.file2 = file;
  }

  compare(){
    if(!this.file1 || !this.file2){
      this.errorMessage = "Lutfen iki imzayi da yukleyin";
      return;
    }
    this.isLoading = true;
    this.errorMessage ="";
    this.result = null;

    this.mainService.verifySignatures(this.file1, this.file2).subscribe({
      next: (response) =>{
        this.result = response;
        this.isLoading = false;
      },
      error: (err) =>{
        this.errorMessage = "Api baglantisi basarisiz";
        this.isLoading=false;
      }
    })
  }
}
