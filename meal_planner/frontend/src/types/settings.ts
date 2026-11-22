export type HouseholdSettings = {
  name: string;
  default_servings: number;
  timezone: string;
  locale: string;
  unit_system: string;
  week_starts_on: number;
  subtract_pantry: boolean;
  auto_shopping: boolean;
  preserve_checked: boolean;
  preserve_manual: boolean;
  auto_consume_pantry: boolean;
};
