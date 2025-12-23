import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MainMenuService {
  private apiUrl = 'http://localhost:8000/api/verify'

  constructor(private http:HttpClient){}

  verifySignatures(file1: File, file2: File): Observable<any> {
    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);
    return this.http.post(this.apiUrl, formData);
  }
}
