import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Route } from '@angular/router';
import { MainMenuService } from '../main-menu-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-main-menu',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './main-menu.html',
  styleUrl: './main-menu.css',
})
export class MainMenu {
  mainMenuForm! : FormGroup;
  errorMessage: string ='';
  isLoading: boolean = false;
  file1: File | null = null;
  file2: File | null = null;
  result: any = null;

  constructor(
    private mainService: MainMenuService,
    private formBuilder: FormBuilder,
    private fb: FormBuilder
  ){
    this.mainMenuForm = this.fb.group({
      file1: [null],
      file2: [null]
    })
  }
  onFileSelected(event:any, fileNo:number){
    const file = event.target.files[0];
    if (fileNo ===1) this.file1 = file;
    else this.file2 = file;
  }

  compare() {
    if (!this.file1 || !this.file2) {
      this.errorMessage = "Lütfen iki imzayı da yükleyin";
      return;
    }

    this.isLoading = true;
    this.errorMessage = "";
    this.result = null;

    this.mainService.verifySignatures(this.file1,this.file2).subscribe({
      next: (response) =>{
        this.result = response;
        this.isLoading = false;
        if (!response.success && response.error) {
          this.errorMessage = response.error || "Bir hata oluştu";
        }
      },
      error: (err) => {
        this.errorMessage = "API bağlantısı başarısız: " + (err.message || "Bilinmeyen hata");
        this.isLoading = false;
        console.error("API Error:", err);
      }
    });
  }
}
