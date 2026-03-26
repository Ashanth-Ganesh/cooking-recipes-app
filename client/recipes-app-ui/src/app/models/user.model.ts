export interface User {
  user_id: number;
  username: string;
  email: string;
  role: 'user' | 'chef' | 'admin';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
