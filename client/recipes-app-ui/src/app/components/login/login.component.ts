import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  identifier = '';
  password = '';
  loading = false;
  error = '';
  returnUrl = '/';

  constructor(private auth: AuthService, private router: Router, private route: ActivatedRoute) {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    if (this.auth.isLoggedIn()) {
      this.router.navigate([this.returnUrl]);
    }
  }

  onSubmit(): void {
    if (!this.identifier || !this.password) {
      this.error = 'Please fill in all fields.';
      return;
    }
    this.loading = true;
    this.error = '';

    this.auth.login(this.identifier, this.password).subscribe({
      next: () => this.router.navigate([this.returnUrl]),
      error: (err) => {
        this.error = err.error?.detail || 'Invalid credentials. Please try again.';
        this.loading = false;
      },
    });
  }
}
