import { ChangeDetectorRef, Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent {

  repoUrl = '';
  repoName = '';
  question = '';
  dbQuestion = '';

  answer: any = null;
  dbResponse: any = null;

  constructor(private api: ApiService,  private cdr: ChangeDetectorRef) {}

  cloneRepository() {

    this.api.cloneRepository(this.repoUrl)
      .subscribe((res: any) => {

        this.repoName = res.repo_name;

        alert('Repository indexed successfully');
      });
  }

  askCodebase() {

    this.api.chatCodebase(
      this.repoName,
      this.question
    ).subscribe((res: any) => {

      this.answer = res.answer;
      this.cdr.detectChanges();
    });
  }

  askDatabase() {

    this.api.askDatabase(
      this.dbQuestion
    ).subscribe((res: any) => {

      this.dbResponse = res;
      this.cdr.detectChanges();
    });
  }
}