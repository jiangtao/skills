export interface VendorSkillMeta {
  official?: boolean
  source: string
  skills: Record<string, string> // sourceSkillName -> outputSkillName
}

/**
 * Repositories to clone as submodules and generate skills from source documentation
 * Type 1: Generated Skills
 */
export const submodules: Record<string, string> = {
  // Add projects here to generate skills from their documentation
  // Example: 'react': 'https://github.com/facebook/react',
}

/**
 * Already generated skills, sync with their `skills/` directory
 * Type 2: Synced Skills
 */
export const vendors: Record<string, VendorSkillMeta> = {
  // Add vendors here that maintain their own skills
  // Example:
  // 'slidev': {
  //   official: true,
  //   source: 'https://github.com/slidevjs/slidev',
  //   skills: {
  //     slidev: 'slidev',
  //   },
  // },
}

/**
 * Hand-written skills with Jerret's preferences/tastes/recommendations
 * Type 3: Manual Skills
 */
export const manual = [
  'jerret',
]
