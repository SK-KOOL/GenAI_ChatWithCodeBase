import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  cloneRepository(repoUrl: string) {

    return this.http.post(
      `${this.baseUrl}/clone-repository`,
      {
        repo_url: repoUrl
      }
    );
  }

  chatCodebase(repoName: string, question: string) {

    return this.http.post(
      `${this.baseUrl}/chat-codebase`,
      {
        repo_name: repoName,
        question: question
      }
    );
  }

  askDatabase(question: string) {

    return this.http.post(
      `${this.baseUrl}/ask-database`,
      {
        question
      }
    );
  }
}