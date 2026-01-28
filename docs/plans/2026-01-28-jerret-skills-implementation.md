# jerret/skills Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a comprehensive Agent Skills collection repository named `jerret/skills` following the specification from [antfu/skills](https://github.com/antfu/skills), supporting hand-written skills, documentation-generated skills, and vendor-synced skills.

**Architecture:**
- Git submodules for source documentation and vendor skill repositories
- TypeScript-based CLI tool for managing submodules and skill synchronization
- Three skill types: Type 1 (generated from docs), Type 2 (synced from vendors), Type 3 (hand-written)
- YAML frontmatter + Markdown content format for all skill files

**Tech Stack:**
- Node.js with TypeScript
- pnpm package manager
- @clack/prompts for interactive CLI
- Git submodules for external repository management

---

## Overview

This plan creates a new Agent Skills collection repository following the architecture established by [antfu/skills](https://github.com/antfu/skills). The repository will:

1. Support three skill types:
   - **Type 1 (Generated)**: Skills generated from project documentation in `sources/` submodules
   - **Type 2 (Synced)**: Skills synced from external repositories that maintain their own skills in `vendor/` submodules
   - **Type 3 (Hand-written)**: Custom skills written manually in `skills/` directory

2. Provide a CLI tool for managing submodules and skill synchronization

3. Follow the [Agent Skills specification](https://agentskills.io/home) with SKILL.md index files and reference-based skill organization

---

## Task 1: Initialize Repository Structure

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `.gitignore`
- Create: `.npmrc`

**Step 1: Create package.json**

```json
{
  "private": true,
  "name": "jerret/skills",
  "version": "0.0.1",
  "packageManager": "pnpm@10.28.2",
  "description": "Jerret's curated collection of Agent Skills",
  "scripts": {
    "lint": "eslint .",
    "start": "node scripts/cli.ts",
    "prepare": "simple-git-hooks && git submodule update --init --recursive"
  },
  "devDependencies": {
    "@antfu/eslint-config": "^7.2.0",
    "@clack/prompts": "^0.11.0",
    "@types/node": "^25.0.10",
    "eslint": "^9.39.2",
    "lint-staged": "^15.5.1",
    "simple-git-hooks": "^2.11.1",
    "typescript": "^5.9.3"
  },
  "simple-git-hooks": {
    "pre-commit": "pnpm lint-staged"
  },
  "lint-staged": {
    "*.{js,ts,mjs,mts}": "eslint --fix"
  }
}
```

**Step 2: Create tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "allowJs": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["node"]
  },
  "include": ["scripts/**/*.ts", "meta.ts"],
  "exclude": ["node_modules", "sources", "vendor", "skills"]
}
```

**Step 3: Create .gitignore**

```
node_modules
*.log
.DS_Store
```

**Step 4: Create .npmrc**

```
shamefully-hoist=true
```

**Step 5: Install dependencies**

Run: `pnpm install`
Expected: All dependencies installed successfully

**Step 6: Initialize git repository**

Run: `git init`
Expected: Empty git repository initialized

**Step 7: Commit initial structure**

```bash
git add package.json tsconfig.json .gitignore .npmrc
git commit -m "feat: initialize repository structure

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Create meta.ts Configuration

**Files:**
- Create: `meta.ts`

**Step 1: Create meta.ts with configuration structure**

```typescript
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
```

**Step 2: Commit meta.ts**

```bash
git add meta.ts
git commit -m "feat: add meta.ts configuration

- Define submodules for Type 1 (generated) skills
- Define vendors for Type 2 (synced) skills
- Define manual list for Type 3 (hand-written) skills

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Create CLI Management Scripts

**Files:**
- Create: `scripts/cli.ts`
- Create: `scripts/.gitkeep`

**Step 1: Create the CLI tool**

Create `scripts/cli.ts` with the following content:

```typescript
import { execSync } from 'node:child_process'
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'
import * as p from '@clack/prompts'
import { manual, submodules, vendors } from '../meta.ts'

const __dirname = dirname(fileURLToPath(import.meta.url))
const root = join(__dirname, '..')

function exec(cmd: string, cwd = root): string {
  return execSync(cmd, { cwd, encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }).trim()
}

function execSafe(cmd: string, cwd = root): string | null {
  try {
    return exec(cmd, cwd)
  }
  catch {
    return null
  }
}

function getGitSha(dir: string): string | null {
  return execSafe('git rev-parse HEAD', dir)
}

function submoduleExists(path: string): boolean {
  const gitmodules = join(root, '.gitmodules')
  if (!existsSync(gitmodules))
    return false
  const content = readFileSync(gitmodules, 'utf-8')
  return content.includes(`path = ${path}`)
}

function getExistingSubmodulePaths(): string[] {
  const gitmodules = join(root, '.gitmodules')
  if (!existsSync(gitmodules))
    return []
  const content = readFileSync(gitmodules, 'utf-8')
  const matches = content.matchAll(/path\s*=\s*(.+)/g)
  return Array.from(matches, match => match[1].trim())
}

function removeSubmodule(submodulePath: string): void {
  execSafe(`git submodule deinit -f ${submodulePath}`)
  const gitModulesPath = join(root, '.git', 'modules', submodulePath)
  if (existsSync(gitModulesPath)) {
    rmSync(gitModulesPath, { recursive: true })
  }
  exec(`git rm -f ${submodulePath}`)
}

interface Project {
  name: string
  url: string
  type: 'source' | 'vendor'
  path: string
}

interface VendorConfig {
  source: string
  skills: Record<string, string>
}

async function initSubmodules(skipPrompt = false) {
  const allProjects: Project[] = [
    ...Object.entries(submodules).map(([name, url]) => ({
      name,
      url,
      type: 'source' as const,
      path: `sources/${name}`,
    })),
    ...Object.entries(vendors).map(([name, config]) => ({
      name,
      url: (config as VendorConfig).source,
      type: 'vendor' as const,
      path: `vendor/${name}`,
    })),
  ]

  const spinner = p.spinner()

  // Check for extra submodules
  const existingSubmodulePaths = getExistingSubmodulePaths()
  const expectedPaths = new Set(allProjects.map(p => p.path))
  const extraSubmodules = existingSubmodulePaths.filter(path => !expectedPaths.has(path))

  if (extraSubmodules.length > 0) {
    p.log.warn(`Found ${extraSubmodules.length} submodule(s) not in meta.ts:`)
    for (const path of extraSubmodules) {
      p.log.message(` - ${path}`)
    }
    const shouldRemove = skipPrompt
      ? true
      : await p.confirm({
          message: 'Remove these extra submodules?',
          initialValue: true,
        })
    if (p.isCancel(shouldRemove)) {
      p.cancel('Cancelled')
      return
    }
    if (shouldRemove) {
      for (const submodulePath of extraSubmodules) {
        spinner.start(`Removing submodule: ${submodulePath}`)
        try {
          removeSubmodule(submodulePath)
          spinner.stop(`Removed: ${submodulePath}`)
        }
        catch (e) {
          spinner.stop(`Failed to remove ${submodulePath}: ${e}`)
        }
      }
    }
  }

  const existingProjects = allProjects.filter(p => submoduleExists(p.path))
  const newProjects = allProjects.filter(p => !submoduleExists(p.path))

  if (newProjects.length === 0) {
    p.log.info('All submodules already initialized')
    return
  }

  const selected = skipPrompt
    ? newProjects
    : await p.multiselect({
        message: 'Select projects to initialize',
        options: newProjects.map(project => ({
          value: project,
          label: `${project.name} (${project.type})`,
          hint: project.url,
        })),
        initialValues: newProjects,
      })

  if (p.isCancel(selected)) {
    p.cancel('Cancelled')
    return
  }

  for (const project of selected as Project[]) {
    spinner.start(`Adding submodule: ${project.name}`)
    const parentDir = join(root, dirname(project.path))
    if (!existsSync(parentDir)) {
      mkdirSync(parentDir, { recursive: true })
    }
    try {
      exec(`git submodule add ${project.url} ${project.path}`)
      spinner.stop(`Added: ${project.name}`)
    }
    catch (e) {
      spinner.stop(`Failed to add ${project.name}: ${e}`)
    }
  }

  p.log.success('Submodules initialized')

  if (existingProjects.length > 0) {
    p.log.info(`Already initialized: ${existingProjects.map(p => p.name).join(', ')}`)
  }
}

async function syncSubmodules() {
  const spinner = p.spinner()

  spinner.start('Updating submodules...')
  try {
    exec('git submodule update --remote --merge')
    spinner.stop('Submodules updated')
  }
  catch (e) {
    spinner.stop(`Failed to update submodules: ${e}`)
    return
  }

  // Sync Type 2 skills
  for (const [vendorName, config] of Object.entries(vendors)) {
    const vendorConfig = config as VendorConfig
    const vendorPath = join(root, 'vendor', vendorName)
    const vendorSkillsPath = join(vendorPath, 'skills')

    if (!existsSync(vendorPath)) {
      p.log.warn(`Vendor submodule not found: ${vendorName}. Run init first.`)
      continue
    }

    if (!existsSync(vendorSkillsPath)) {
      p.log.warn(`No skills directory in vendor/${vendorName}/skills/`)
      continue
    }

    for (const [sourceSkillName, outputSkillName] of Object.entries(vendorConfig.skills)) {
      const sourceSkillPath = join(vendorSkillsPath, sourceSkillName)
      const outputPath = join(root, 'skills', outputSkillName)

      if (!existsSync(sourceSkillPath)) {
        p.log.warn(`Skill not found: vendor/${vendorName}/skills/${sourceSkillName}`)
        continue
      }

      spinner.start(`Syncing skill: ${sourceSkillName} → ${outputSkillName}`)

      if (existsSync(outputPath)) {
        rmSync(outputPath, { recursive: true })
      }
      mkdirSync(outputPath, { recursive: true })

      const files = readdirSync(sourceSkillPath, { recursive: true, withFileTypes: true })
      for (const file of files) {
        if (file.isFile()) {
          const fullPath = join(file.parentPath, file.name)
          const relativePath = fullPath.replace(sourceSkillPath, '')
          const destPath = join(outputPath, relativePath)
          const destDir = dirname(destPath)
          if (!existsSync(destDir)) {
            mkdirSync(destDir, { recursive: true })
          }
          cpSync(fullPath, destPath)
        }
      }

      const licenseNames = ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'license', 'license.md', 'license.txt']
      for (const licenseName of licenseNames) {
        const licensePath = join(vendorPath, licenseName)
        if (existsSync(licensePath)) {
          cpSync(licensePath, join(outputPath, 'LICENSE.md'))
          break
        }
      }

      const sha = getGitSha(vendorPath)
      const syncPath = join(outputPath, 'SYNC.md')
      const date = new Date().toISOString().split('T')[0]
      const syncContent = `# Sync Info

- **Source:** \`vendor/${vendorName}/skills/${sourceSkillName}\`
- **Git SHA:** \`${sha}\`
- **Synced:** ${date}
`
      writeFileSync(syncPath, syncContent)
      spinner.stop(`Synced: ${sourceSkillName} → ${outputSkillName}`)
    }
  }

  p.log.success('All skills synced')
}

async function checkUpdates() {
  const spinner = p.spinner()

  spinner.start('Fetching remote changes...')
  try {
    exec('git submodule foreach git fetch')
    spinner.stop('Fetched remote changes')
  }
  catch (e) {
    spinner.stop(`Failed to fetch: ${e}`)
    return
  }

  const updates: { name: string, type: string, behind: number }[] = []

  for (const name of Object.keys(submodules)) {
    const path = join(root, 'sources', name)
    if (!existsSync(path))
      continue
    const behind = execSafe('git rev-list HEAD..@{u} --count', path)
    if (behind && Number.parseInt(behind) > 0) {
      updates.push({ name, type: 'source', behind: Number.parseInt(behind) })
    }
  }

  for (const [name, config] of Object.entries(vendors)) {
    const vendorConfig = config as VendorConfig
    const path = join(root, 'vendor', name)
    if (!existsSync(path))
      continue
    const behind = execSafe('git rev-list HEAD..@{u} --count', path)
    if (behind && Number.parseInt(behind) > 0) {
      const skillNames = Object.values(vendorConfig.skills).join(', ')
      updates.push({ name: `${name} (${skillNames})`, type: 'vendor', behind: Number.parseInt(behind) })
    }
  }

  if (updates.length === 0) {
    p.log.success('All submodules are up to date')
  }
  else {
    p.log.info('Updates available:')
    for (const update of updates) {
      p.log.message(` ${update.name} (${update.type}): ${update.behind} commits behind`)
    }
  }
}

function getExpectedSkillNames(): Set<string> {
  const expected = new Set<string>()
  for (const name of Object.keys(submodules)) {
    expected.add(name)
  }
  for (const config of Object.values(vendors)) {
    const vendorConfig = config as VendorConfig
    for (const outputName of Object.values(vendorConfig.skills)) {
      expected.add(outputName)
    }
  }
  for (const name of manual) {
    expected.add(name)
  }
  return expected
}

function getExistingSkillNames(): string[] {
  const skillsDir = join(root, 'skills')
  if (!existsSync(skillsDir))
    return []
  return readdirSync(skillsDir, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
}

async function cleanup(skipPrompt = false) {
  const spinner = p.spinner()
  let hasChanges = false

  const allProjects: Project[] = [
    ...Object.entries(submodules).map(([name, url]) => ({
      name,
      url,
      type: 'source' as const,
      path: `sources/${name}`,
    })),
    ...Object.entries(vendors).map(([name, config]) => ({
      name,
      url: (config as VendorConfig).source,
      type: 'vendor' as const,
      path: `vendor/${name}`,
    })),
  ]

  const existingSubmodulePaths = getExistingSubmodulePaths()
  const expectedSubmodulePaths = new Set(allProjects.map(p => p.path))
  const extraSubmodules = existingSubmodulePaths.filter(path => !expectedSubmodulePaths.has(path))

  if (extraSubmodules.length > 0) {
    p.log.warn(`Found ${extraSubmodules.length} submodule(s) not in meta.ts:`)
    for (const path of extraSubmodules) {
      p.log.message(` - ${path}`)
    }
    const shouldRemove = skipPrompt
      ? true
      : await p.confirm({
          message: 'Remove these extra submodules?',
          initialValue: true,
        })
    if (p.isCancel(shouldRemove)) {
      p.cancel('Cancelled')
      return
    }
    if (shouldRemove) {
      hasChanges = true
      for (const submodulePath of extraSubmodules) {
        spinner.start(`Removing submodule: ${submodulePath}`)
        try {
          removeSubmodule(submodulePath)
          spinner.stop(`Removed: ${submodulePath}`)
        }
        catch (e) {
          spinner.stop(`Failed to remove ${submodulePath}: ${e}`)
        }
      }
    }
  }

  const existingSkills = getExistingSkillNames()
  const expectedSkills = getExpectedSkillNames()
  const extraSkills = existingSkills.filter(name => !expectedSkills.has(name))

  if (extraSkills.length > 0) {
    p.log.warn(`Found ${extraSkills.length} skill(s) not in meta.ts:`)
    for (const name of extraSkills) {
      p.log.message(` - skills/${name}`)
    }
    const shouldRemove = skipPrompt
      ? true
      : await p.confirm({
          message: 'Remove these extra skills?',
          initialValue: true,
        })
    if (p.isCancel(shouldRemove)) {
      p.cancel('Cancelled')
      return
    }
    if (shouldRemove) {
      hasChanges = true
      for (const skillName of extraSkills) {
        spinner.start(`Removing skill: ${skillName}`)
        try {
          rmSync(join(root, 'skills', skillName), { recursive: true })
          spinner.stop(`Removed: skills/${skillName}`)
        }
        catch (e) {
          spinner.stop(`Failed to remove skills/${skillName}: ${e}`)
        }
      }
    }
  }

  if (!hasChanges && extraSubmodules.length === 0 && extraSkills.length === 0) {
    p.log.success('Everything is clean, no unused submodules or skills found')
  }
  else if (hasChanges) {
    p.log.success('Cleanup completed')
  }
}

async function main() {
  const args = process.argv.slice(2)
  const skipPrompt = args.includes('-y') || args.includes('--yes')
  const command = args.find(arg => !arg.startsWith('-'))

  if (command === 'init') {
    p.intro('Skills Manager - Init')
    await initSubmodules(skipPrompt)
    p.outro('Done')
    return
  }

  if (command === 'sync') {
    p.intro('Skills Manager - Sync')
    await syncSubmodules()
    p.outro('Done')
    return
  }

  if (command === 'check') {
    p.intro('Skills Manager - Check')
    await checkUpdates()
    p.outro('Done')
    return
  }

  if (command === 'cleanup') {
    p.intro('Skills Manager - Cleanup')
    await cleanup(skipPrompt)
    p.outro('Done')
    return
  }

  if (skipPrompt) {
    p.log.error('Command required when using -y flag')
    p.log.info('Available commands: init, sync, check, cleanup')
    process.exit(1)
  }

  p.intro('Skills Manager')

  const action = await p.select({
    message: 'What would you like to do?',
    options: [
      { value: 'sync', label: 'Sync submodules', hint: 'Pull latest and sync Type 2 skills' },
      { value: 'init', label: 'Init submodules', hint: 'Add new submodules' },
      { value: 'check', label: 'Check updates', hint: 'See available updates' },
      { value: 'cleanup', label: 'Cleanup', hint: 'Remove unused submodules and skills' },
    ],
  })

  if (p.isCancel(action)) {
    p.cancel('Cancelled')
    process.exit(0)
  }

  switch (action) {
    case 'init':
      await initSubmodules()
      break
    case 'sync':
      await syncSubmodules()
      break
    case 'check':
      await checkUpdates()
      break
    case 'cleanup':
      await cleanup()
      break
  }

  p.outro('Done')
}

main().catch(console.error)
```

**Step 2: Create .gitkeep in scripts directory**

```bash
touch scripts/.gitkeep
```

**Step 3: Commit CLI scripts**

```bash
git add scripts/
git commit -m "feat: add CLI management scripts

- Add init command for adding submodules
- Add sync command for syncing vendor skills
- Add check command for checking updates
- Add cleanup command for removing unused submodules/skills

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 4: Create ESLint Configuration

**Files:**
- Create: `eslint.config.js`

**Step 1: Create eslint.config.js**

```javascript
import antfu from '@antfu/eslint-config'

export default antfu({
  typescript: true,
  ignores: [
    'node_modules',
    'sources',
    'vendor',
    'skills',
  ],
})
```

**Step 2: Commit ESLint config**

```bash
git add eslint.config.js
git commit -m "feat: add ESLint configuration

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 5: Create Initial Hand-Written Skill

**Files:**
- Create: `skills/jerret/skill.md`
- Create: `skills/jerret/references/introduction.md`

**Step 1: Create skills directory structure**

```bash
mkdir -p skills/jerret/references
```

**Step 2: Create main skill.md**

```markdown
---
name: jerret
description: Jerret's development preferences and best practices
metadata:
  author: Jerret
  version: "2026.1.28"
---

> Jerret's personal development preferences and best practices for software projects.

## Overview

This skill contains Jerret's preferences for:
- Code style and formatting
- Project structure
- Tooling choices
- Best practices

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Introduction | About this skill collection | [introduction](references/introduction.md) |
```

**Step 3: Create introduction.md**

```markdown
---
name: introduction
description: Introduction to Jerret's skill collection
---

# About This Collection

This is Jerret's curated collection of Agent Skills, reflecting personal preferences and best practices for software development.

## Philosophy

- **Pragmatism over dogmatism**: Choose tools that work for the specific problem
- **Simplicity**: Avoid over-engineering and unnecessary complexity
- **Documentation first**: Write code that is self-documenting with clear intent

## Preferences

### Languages
- TypeScript for type safety
- Rust for systems programming
- Python for scripting and data

### Frameworks
- Choose based on project needs
- Prefer minimal, flexible options

### Tooling
- pnpm for package management
- ESLint for linting
- Git for version control
```

**Step 4: Commit initial skill**

```bash
git add skills/
git commit -m "feat: add initial jerret hand-written skill

- Add skill.md with overview
- Add introduction reference

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 6: Create Documentation

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `LICENSE.md`

**Step 1: Create README.md**

```markdown
# Jerret's Skills

A curated collection of [Agent Skills](https://agentskills.io/home) reflecting Jerret's preferences, experience, and best practices.

## Installation

```bash
pnpx skills add jerret/skills
```

or to install it globally:

```bash
pnpx skills add jerret/skills -g
```

Learn more about the CLI usage at [skills](https://github.com/agentskills/skills).

## Skills

### Hand-maintained Skills

> Opinionated

Manually maintained with preferred tools, setup conventions, and best practices.

| Skill | Description |
|-------|-------------|
| [jerret](skills/jerret) | Jerret's preferences and best practices |

### Skills Generated from Official Documentation

> Unopinionated but with tilted focus

Generated from official documentation.

| Skill | Description | Source |
|-------|-------------|--------|
| *(Coming soon)* | | |

### Vendored Skills

Synced from external repositories that maintain their own skills.

| Skill | Description | Source |
|-------|-------------|--------|
| *(Coming soon)* | | |

## What Makes This Collection Different?

This collection uses git submodules to directly reference source documentation, providing more reliable context and allowing skills to stay up-to-date with upstream changes.

## Generate Your Own Skills

Fork this project to create your own customized skill collection.

1. Fork or clone this repository
2. Install dependencies: `pnpm install`
3. Update `meta.ts` with your own projects and skill sources
4. Run `pnpm start cleanup` to remove existing submodules and skills
5. Run `pnpm start init` to clone the submodules
6. Run `pnpm start sync` to sync vendored skills
7. Ask your agent to "generate skills for <project>"

See [AGENTS.md](AGENTS.md) for detailed generation guidelines.

## License

Skills and the scripts in this repository are [MIT](LICENSE.md) licensed.

Vendored skills from external repositories retain their original licenses - see each skill directory for details.
```

**Step 2: Create AGENTS.md**

```markdown
# Skills Generator

Generate [Agent Skills](https://agentskills.io/home) from project documentation.

## Skill Source Types

### Type 1: Generated Skills (`sources/`)

For OSS projects **without existing skills**. We clone the repo as a submodule and generate skills from their documentation.

**Workflow:** Read docs → Understand → Generate skills

**Source:** `sources/{project}/docs/`

### Type 2: Synced Skills (`vendor/`)

For projects that **already maintain their own skills**. We clone their repo as a submodule and sync specified skills.

**Workflow:** Pull updates → Copy specified skills (with optional renaming)

**Source:** `vendor/{project}/skills/{skill-name}/`

**Config:** Each vendor specifies which skills to sync in `meta.ts`

### Type 3: Hand-written Skills

Skills written manually with personal preferences and best practices.

## Repository Structure

```
.
├── meta.ts              # Project metadata (repos & URLs)
├── scripts/             # CLI management scripts
│   └── cli.ts          # Main CLI entry point
│
├── sources/             # Type 1: OSS repos (generate from docs)
│   └── {project}/
│       └── docs/       # Read documentation from here
│
├── vendor/              # Type 2: Projects with existing skills (sync only)
│   └── {project}/
│       └── skills/
│           └── {skill-name}/  # Individual skills to sync
│
└── skills/              # Output directory (generated or synced)
    └── {output-name}/
        ├── skill.md    # Index of all skills
        ├── GENERATION.md  # Tracking metadata (for generated skills)
        ├── SYNC.md     # Tracking metadata (for synced skills)
        └── references/
            └── *.md    # Individual skill files
```

## Workflows

### For Generated Skills (Type 1)

#### Adding a New Project

1. Add entry to `meta.ts` in the `submodules` object
2. Run `pnpm start init -y` to clone the submodule
3. Follow generation guide to create the skills

#### Creating New Skills

1. Read source docs from `sources/{project}/docs/`
2. Understand the documentation thoroughly
3. Create skill files in `skills/{project}/references/`
4. Create `skill.md` index listing all skills
5. Create `GENERATION.md` with the source git SHA

#### Updating Generated Skills

1. Check git diff since the SHA in `GENERATION.md`
2. Update affected skill files based on changes
3. Update `skill.md` with the new version
4. Update `GENERATION.md` with new SHA

### For Synced Skills (Type 2)

#### Initial Sync

1. Copy specified skills from `vendor/{project}/skills/{skill-name}/` to `skills/{output-name}/`
2. Create `SYNC.md` with the vendor git SHA

#### Updating Synced Skills

1. Check git diff since the SHA in `SYNC.md`
2. Copy changed files from vendor to output
3. Update `SYNC.md` with new SHA

**Note:** Do NOT modify synced skills manually. Contribute changes upstream.

## File Formats

### `skill.md`

Index file listing all skills with brief descriptions.

```markdown
---
name: {name}
description: {description}
metadata:
  author: Jerret
  version: "2026.1.28"
---

> Brief summary/context

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Topic Name | Description | [reference-name](references/file.md) |
```

### `GENERATION.md`

Tracking metadata for generated skills (Type 1).

```markdown
# Generation Info

- **Source:** `sources/{project}`
- **Git SHA:** `abc123def456...`
- **Generated:** 2024-01-15
```

### `SYNC.md`

Tracking metadata for synced skills (Type 2).

```markdown
# Sync Info

- **Source:** `vendor/{project}/skills/{skill-name}`
- **Git SHA:** `abc123def456...`
- **Synced:** 2024-01-15
```

### `references/*.md`

Individual skill files. One concept per file.

```markdown
---
name: {name}
description: {description}
---

# {Concept Name}

Brief description.

## Usage

Code examples and patterns.

## Key Points

- Important detail 1
- Important detail 2
```
```

**Step 3: Create LICENSE.md**

```markdown
MIT License

Copyright (c) 2026 Jerret

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Step 4: Commit documentation**

```bash
git add README.md AGENTS.md LICENSE.md
git commit -m "docs: add project documentation

- Add README.md with installation and usage
- Add AGENTS.md with generation guidelines
- Add MIT LICENSE

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 7: Final Setup and Verification

**Files:**
- Modify: None (verification steps)

**Step 1: Run linter to verify code quality**

Run: `pnpm lint`
Expected: No linting errors

**Step 2: Test CLI interactive mode**

Run: `pnpm start`
Expected: Interactive menu appears with options for init, sync, check, cleanup

**Step 3: Test CLI commands**

Run: `pnpm start init -y`
Expected: "All submodules already initialized" (since meta.ts is empty)

Run: `pnpm start check`
Expected: "All submodules are up to date"

Run: `pnpm start cleanup -y`
Expected: "Everything is clean, no unused submodules or skills found"

**Step 4: Verify skill structure**

Run: `ls -la skills/jerret/`
Expected: Should show skill.md, references/ directory

**Step 5: Create initial git tag**

Run: `git tag -a v0.0.1 -m "Initial release of jerret/skills"`

**Step 6: Final verification commit**

```bash
git add .
git commit -m "chore: complete initial project setup

- All core infrastructure in place
- CLI tool fully functional
- Initial hand-written skill created
- Documentation complete

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Summary

This implementation plan creates a fully functional Agent Skills collection repository `jerret/skills` that:

1. **Supports three skill types**:
   - Type 1: Generated from project documentation in `sources/` submodules
   - Type 2: Synced from external repositories in `vendor/` submodules
   - Type 3: Hand-written skills in `skills/` directory

2. **Provides CLI management**:
   - `pnpm start init` - Add new submodules
   - `pnpm start sync` - Sync vendor skills
   - `pnpm start check` - Check for updates
   - `pnpm start cleanup` - Remove unused resources

3. **Follows Agent Skills specification**:
   - YAML frontmatter in skill.md files
   - Reference-based skill organization
   - GENERATION.md/SYNC.md tracking metadata

4. **Ready for extension**:
   - Add projects to `meta.ts` submodules for Type 1
   - Add vendors to `meta.ts` vendors for Type 2
   - Create new directories in `skills/` for Type 3

After completion, the repository will be ready to publish to GitHub and install via `pnpx skills add jerret/skills`.
