import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import { AuthResponse } from '../models/user.model';

const mockAuthResponse: AuthResponse = {
  access_token: 'mock-token',
  token_type: 'bearer',
  user: { user_id: 1, username: 'testuser', email: 'test@test.com', role: 'user' },
};

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [AuthService, provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('isLoggedIn', () => {
    it('returns false when no token in localStorage', () => {
      expect(service.isLoggedIn()).toBe(false);
    });

    it('returns true when token exists in localStorage', () => {
      localStorage.setItem('token', 'some-token');
      expect(service.isLoggedIn()).toBe(true);
    });
  });

  describe('getToken', () => {
    it('returns null when no token stored', () => {
      expect(service.getToken()).toBeNull();
    });

    it('returns token string when stored', () => {
      localStorage.setItem('token', 'abc123');
      expect(service.getToken()).toBe('abc123');
    });
  });

  describe('getCurrentUser', () => {
    it('returns null when no user is stored', () => {
      expect(service.getCurrentUser()).toBeNull();
    });

    it('loads user from localStorage on construction', () => {
      const user = { user_id: 5, username: 'preloaded', email: 'pre@test.com', role: 'user' as const };
      localStorage.setItem('user', JSON.stringify(user));
      // Re-create service so constructor reads updated localStorage
      TestBed.resetTestingModule();
      TestBed.configureTestingModule({
        providers: [AuthService, provideHttpClient(), provideHttpClientTesting()],
      });
      const freshService = TestBed.inject(AuthService);
      expect(freshService.getCurrentUser()).toEqual(user);
    });
  });

  describe('isChefOrAdmin', () => {
    it('returns false when no user is logged in', () => {
      expect(service.isChefOrAdmin()).toBe(false);
    });

    it('returns false after logging in as a regular user', () => {
      service.login('testuser', 'password').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(mockAuthResponse);
      expect(service.isChefOrAdmin()).toBe(false);
    });

    it('returns true after logging in as a chef', () => {
      const chefResponse: AuthResponse = {
        ...mockAuthResponse,
        user: { ...mockAuthResponse.user, role: 'chef' },
      };
      service.login('chefuser', 'password').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(chefResponse);
      expect(service.isChefOrAdmin()).toBe(true);
    });

    it('returns true after logging in as an admin', () => {
      const adminResponse: AuthResponse = {
        ...mockAuthResponse,
        user: { ...mockAuthResponse.user, role: 'admin' },
      };
      service.login('adminuser', 'password').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(adminResponse);
      expect(service.isChefOrAdmin()).toBe(true);
    });
  });

  describe('login', () => {
    it('POSTs to the login endpoint with correct body', () => {
      service.login('testuser', 'password123').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({ username_or_email: 'testuser', password: 'password123' });
      req.flush(mockAuthResponse);
    });

    it('stores token in localStorage after successful login', () => {
      service.login('testuser', 'password123').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(mockAuthResponse);
      expect(localStorage.getItem('token')).toBe('mock-token');
    });

    it('stores user in localStorage after successful login', () => {
      service.login('testuser', 'password123').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(mockAuthResponse);
      expect(JSON.parse(localStorage.getItem('user')!)).toEqual(mockAuthResponse.user);
    });

    it('updates currentUser$ observable after login', () => {
      let emitted: any;
      service.currentUser$.subscribe((u) => (emitted = u));
      service.login('testuser', 'password123').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/login');
      req.flush(mockAuthResponse);
      expect(emitted).toEqual(mockAuthResponse.user);
    });
  });

  describe('signup', () => {
    it('POSTs to the signup endpoint with correct body', () => {
      service.signup('newuser', 'new@test.com', 'password123').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/signup');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({
        username: 'newuser',
        email: 'new@test.com',
        password: 'password123',
        role: 'user',
      });
      req.flush(mockAuthResponse);
    });

    it('sends custom role when provided', () => {
      service.signup('chefuser', 'chef@test.com', 'password123', 'chef').subscribe();
      const req = httpMock.expectOne('http://localhost:8000/api/auth/signup');
      expect(req.request.body.role).toBe('chef');
      req.flush(mockAuthResponse);
    });
  });

  describe('logout', () => {
    it('removes token from localStorage', () => {
      localStorage.setItem('token', 'some-token');
      service.logout();
      expect(localStorage.getItem('token')).toBeNull();
    });

    it('removes user from localStorage', () => {
      localStorage.setItem('user', JSON.stringify(mockAuthResponse.user));
      service.logout();
      expect(localStorage.getItem('user')).toBeNull();
    });

    it('sets currentUser$ to null', () => {
      let emitted: any = 'initial';
      service.currentUser$.subscribe((u) => (emitted = u));
      service.logout();
      expect(emitted).toBeNull();
    });

    it('makes isLoggedIn return false', () => {
      localStorage.setItem('token', 'some-token');
      service.logout();
      expect(service.isLoggedIn()).toBe(false);
    });
  });
});
