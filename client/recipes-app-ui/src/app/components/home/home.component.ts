import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent {
  searchQuery = '';

  cuisines = [
    { name: 'Italian', emoji: '🍕' },
    { name: 'Asian', emoji: '🍜' },
    { name: 'Mexican', emoji: '🌮' },
    { name: 'Indian', emoji: '🍛' },
    { name: 'American', emoji: '🍔' },
    { name: 'Mediterranean', emoji: '🫒' },
    { name: 'French', emoji: '🥐' },
    { name: 'Japanese', emoji: '🍱' },
  ];

  categories = [
    { label: 'Quick & Easy', icon: '⚡', filter: 'max_ready_time=30' },
    { label: 'Vegetarian', icon: '🥗', filter: 'diet=vegetarian' },
    { label: 'Vegan', icon: '🌱', filter: 'diet=vegan' },
    { label: 'Gluten-Free', icon: '🌾', filter: 'diet=gluten+free' },
    { label: 'Breakfast', icon: '🥞', filter: 'meal_type=breakfast' },
    { label: 'Desserts', icon: '🍰', filter: 'meal_type=dessert' },
  ];

  constructor(public router: Router) {}

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/recipes'], { queryParams: { query: this.searchQuery.trim() } });
    } else {
      this.router.navigate(['/recipes']);
    }
  }

  navigateCuisine(cuisine: string): void {
    this.router.navigate(['/recipes'], { queryParams: { cuisine } });
  }

  navigateCategory(filter: string): void {
    const params: Record<string, string> = {};
    filter.split('&').forEach((part) => {
      const [key, val] = part.split('=');
      params[key] = decodeURIComponent(val);
    });
    this.router.navigate(['/recipes'], { queryParams: params });
  }

  parseFilter(filter: string): Record<string, string> {
    const params: Record<string, string> = {};
    filter.split('&').forEach((part) => {
      const [key, val] = part.split('=');
      params[key] = decodeURIComponent(val);
    });
    return params;
  }
}
