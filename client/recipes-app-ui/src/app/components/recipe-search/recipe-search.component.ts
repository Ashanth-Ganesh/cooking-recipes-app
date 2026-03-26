import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeCardComponent } from '../recipe-card/recipe-card.component';
import { RecipeService } from '../../services/recipe.service';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { Recipe, SearchResult } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-search',
  standalone: true,
  imports: [FormsModule, CommonModule, RecipeCardComponent],
  templateUrl: './recipe-search.component.html',
  styleUrl: './recipe-search.component.css',
})
export class RecipeSearchComponent implements OnInit {
  // Search state
  query = '';
  cuisine = '';
  diet = '';
  intolerances: string[] = [];
  meal_type = '';
  max_ready_time: number | null = null;
  ingredients = '';

  // Results
  recipes: Recipe[] = [];
  totalResults = 0;
  currentPage = 0;
  readonly pageSize = 12;
  loading = false;
  error = '';
  hasSearched = false;

  // Filter options
  cuisineOptions = [
    'African', 'American', 'Asian', 'British', 'Cajun', 'Caribbean',
    'Chinese', 'Eastern European', 'European', 'French', 'German',
    'Greek', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish',
    'Korean', 'Latin American', 'Mediterranean', 'Mexican',
    'Middle Eastern', 'Nordic', 'Southern', 'Spanish', 'Thai', 'Vietnamese',
  ];

  dietOptions = [
    { value: 'gluten free', label: 'Gluten Free' },
    { value: 'ketogenic', label: 'Ketogenic' },
    { value: 'vegetarian', label: 'Vegetarian' },
    { value: 'lacto-vegetarian', label: 'Lacto-Vegetarian' },
    { value: 'ovo-vegetarian', label: 'Ovo-Vegetarian' },
    { value: 'vegan', label: 'Vegan' },
    { value: 'pescetarian', label: 'Pescetarian' },
    { value: 'paleo', label: 'Paleo' },
    { value: 'primal', label: 'Primal' },
    { value: 'whole30', label: 'Whole30' },
  ];

  intoleranceOptions = [
    'Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut',
    'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Sulfite', 'Tree Nut', 'Wheat',
  ];

  mealTypeOptions = [
    { value: 'main course', label: 'Main Course' },
    { value: 'side dish', label: 'Side Dish' },
    { value: 'dessert', label: 'Dessert' },
    { value: 'appetizer', label: 'Appetizer' },
    { value: 'salad', label: 'Salad' },
    { value: 'bread', label: 'Bread' },
    { value: 'breakfast', label: 'Breakfast' },
    { value: 'soup', label: 'Soup' },
    { value: 'beverage', label: 'Beverage' },
    { value: 'sauce', label: 'Sauce' },
    { value: 'snack', label: 'Snack' },
    { value: 'drink', label: 'Drink' },
  ];

  timeOptions = [
    { value: 15, label: 'Under 15 min' },
    { value: 30, label: 'Under 30 min' },
    { value: 45, label: 'Under 45 min' },
    { value: 60, label: 'Under 1 hour' },
    { value: 120, label: 'Under 2 hours' },
  ];

  filtersOpen = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private recipeService: RecipeService,
    private favorites: FavoritesService,
    private auth: AuthService
  ) {}

  ngOnInit(): void {
    if (this.auth.isLoggedIn()) {
      this.favorites.load().subscribe();
    }
    this.route.queryParams.subscribe((params) => {
      this.query = params['query'] || '';
      this.cuisine = params['cuisine'] || '';
      this.diet = params['diet'] || '';
      this.meal_type = params['meal_type'] || '';
      this.max_ready_time = params['max_ready_time'] ? +params['max_ready_time'] : null;
      this.ingredients = params['ingredients'] || '';
      this.intolerances = params['intolerances'] ? params['intolerances'].split(',') : [];
      this.currentPage = 0;
      this.search();
    });
  }

  search(): void {
    this.loading = true;
    this.error = '';
    this.hasSearched = true;

    this.recipeService
      .search({
        query: this.query,
        cuisine: this.cuisine,
        diet: this.diet,
        intolerances: this.intolerances.join(','),
        meal_type: this.meal_type,
        max_ready_time: this.max_ready_time,
        ingredients: this.ingredients,
        number: this.pageSize,
        offset: this.currentPage * this.pageSize,
      })
      .subscribe({
        next: (result: SearchResult) => {
          this.recipes = result.results || [];
          this.totalResults = result.totalResults || 0;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to fetch recipes. Please try again.';
          this.loading = false;
        },
      });
  }

  applyFilters(): void {
    this.currentPage = 0;
    this.search();
    this.filtersOpen = false;
  }

  clearFilters(): void {
    this.query = '';
    this.cuisine = '';
    this.diet = '';
    this.meal_type = '';
    this.max_ready_time = null;
    this.ingredients = '';
    this.intolerances = [];
    this.currentPage = 0;
    this.search();
  }

  toggleIntolerance(item: string): void {
    const idx = this.intolerances.indexOf(item.toLowerCase());
    if (idx > -1) {
      this.intolerances.splice(idx, 1);
    } else {
      this.intolerances.push(item.toLowerCase());
    }
  }

  hasIntolerance(item: string): boolean {
    return this.intolerances.includes(item.toLowerCase());
  }

  nextPage(): void {
    if ((this.currentPage + 1) * this.pageSize < this.totalResults) {
      this.currentPage++;
      this.search();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  prevPage(): void {
    if (this.currentPage > 0) {
      this.currentPage--;
      this.search();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  get totalPages(): number {
    return Math.ceil(this.totalResults / this.pageSize);
  }

  get hasActiveFilters(): boolean {
    return !!(this.cuisine || this.diet || this.meal_type || this.max_ready_time || this.ingredients || this.intolerances.length);
  }
}
