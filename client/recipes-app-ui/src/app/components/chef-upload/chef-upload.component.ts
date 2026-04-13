import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FavoritesService } from '../../services/favorites.service';

@Component({
  selector: 'app-chef-upload',
  standalone: true,
  imports: [FormsModule, RouterLink, CommonModule],
  templateUrl: './chef-upload.component.html',
  styleUrl: './chef-upload.component.css',
})
export class ChefUploadComponent {
  recipeName = '';
  imageUrl = '';
  readyInMinutes: number | null = null;
  servings: number | null = null;
  recipeType = '';
  recipeCuisine = '';
  instructions = '';
  ingredients: string[] = [''];

  loading = false;
  error = '';
  success = '';

  cuisineOptions = [
    'American', 'Asian', 'British', 'Caribbean', 'Chinese', 'European',
    'French', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean',
    'Mediterranean', 'Mexican', 'Middle Eastern', 'Spanish', 'Thai', 'Vietnamese',
  ];

  typeOptions = [
    'main course', 'side dish', 'dessert', 'appetizer', 'salad',
    'bread', 'breakfast', 'soup', 'beverage', 'sauce', 'snack',
  ];

  constructor(private favorites: FavoritesService, private router: Router) {}

  addIngredient(): void {
    this.ingredients.push('');
  }

  removeIngredient(idx: number): void {
    if (this.ingredients.length > 1) {
      this.ingredients.splice(idx, 1);
    }
  }

  trackByIndex(idx: number): number {
    return idx;
  }

  onSubmit(): void {
    if (!this.recipeName.trim()) {
      this.error = 'Recipe name is required.';
      return;
    }
    if (!this.instructions.trim()) {
      this.error = 'Instructions are required.';
      return;
    }
    const filteredIngredients = this.ingredients.filter((i) => i.trim());
    if (filteredIngredients.length === 0) {
      this.error = 'At least one ingredient is required.';
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = '';

    this.favorites
      .addCustom({
        recipe_name: this.recipeName.trim(),
        image_url: this.imageUrl.trim() || null,
        ready_in_minutes: this.readyInMinutes,
        servings: this.servings,
        recipe_ingredients: filteredIngredients,
        recipe_instructions: this.instructions.trim(),
        recipe_type: this.recipeType || null,
        recipe_cuisine: this.recipeCuisine || null,
      })
      .subscribe({
        next: () => {
          this.success = 'Recipe added successfully!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/favorites']), 1500);
        },
        error: (err) => {
          this.error = err.error?.detail || 'Failed to add recipe.';
          this.loading = false;
        },
      });
  }
}
