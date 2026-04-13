import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { User, AuthResponse } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API = 'http://localhost:8000/api/auth';
  private userSubject = new BehaviorSubject<User | null>(null);
  currentUser$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try { this.userSubject.next(JSON.parse(userStr)); } catch {}
    }
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getCurrentUser(): User | null {
    return this.userSubject.value;
  }

  isChefOrAdmin(): boolean {
    const user = this.getCurrentUser();
    return user ? ['chef', 'admin'].includes(user.role) : false;
  }

  login(usernameOrEmail: string, password: string): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${this.API}/login`, {
        username_or_email: usernameOrEmail,
        password,
      })
      .pipe(tap((res) => this.storeAuth(res)));
  }

  signup(username: string, email: string, password: string, role = 'user'): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${this.API}/signup`, { username, email, password, role })
      .pipe(tap((res) => this.storeAuth(res)));
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.userSubject.next(null);
  }

  private storeAuth(res: AuthResponse): void {
    localStorage.setItem('token', res.access_token);
    localStorage.setItem('user', JSON.stringify(res.user));
    this.userSubject.next(res.user);
  }
}
