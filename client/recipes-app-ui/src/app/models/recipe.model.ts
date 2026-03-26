export interface Recipe {
  id: number;
  title: string;
  image: string;
  readyInMinutes: number;
  servings: number;
  summary?: string;
  cuisines?: string[];
  dishTypes?: string[];
  diets?: string[];
  instructions?: string;
  extendedIngredients?: Ingredient[];
  nutrition?: Nutrition;
  sourceUrl?: string;
  vegetarian?: boolean;
  vegan?: boolean;
  glutenFree?: boolean;
  dairyFree?: boolean;
  cheap?: boolean;
  spoonacularScore?: number;
  healthScore?: number;
}

export interface Ingredient {
  id: number;
  name: string;
  original: string;
  amount: number;
  unit: string;
  image?: string;
}

export interface Nutrition {
  nutrients: Nutrient[];
  caloricBreakdown?: {
    percentProtein: number;
    percentFat: number;
    percentCarbs: number;
  };
}

export interface Nutrient {
  name: string;
  amount: number;
  unit: string;
  percentOfDailyNeeds?: number;
}

export interface SearchResult {
  results: Recipe[];
  offset: number;
  number: number;
  totalResults: number;
}

export interface FavoriteRecipe {
  recipe_id: number;
  spoonacular_id: number | null;
  recipe_name: string;
  image_url: string | null;
  ready_in_minutes: number | null;
  servings: number | null;
  is_custom: boolean;
  recipe_type: string | null;
  recipe_cuisine: string | null;
}

export interface SearchFilters {
  query: string;
  cuisine: string;
  diet: string;
  intolerances: string[];
  meal_type: string;
  max_ready_time: number | null;
  ingredients: string;
}
