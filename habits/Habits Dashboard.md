I built a habit tracker within Obsidian leveraging a ([[Template - Daily Habits|Custom Template]]) for tracking habits in a daily YYYY-MM-DD note and then rendering the results via the Heatmap Calendar plug-in.

This works great, however I discovered the [Awesome Habits](https://www.awesome-habits.com/) app via SetApp, which is also available on iOS and I've migrated there. Keeping this content as an archived project for posterity.

Below are the snippets I've removed from my [[Dashboard]].

```
# Habits

<table width="100%">
    <tr>
        <td width="50%"><center><code>="[[" + "Journal/" + dateformat(date(today), "yyyy-MM-dd") + "|Journal]]"</code></center></td>
        <td width="50%"><center><code>="[[" + "Habits/Habits - " + dateformat(date(today), "yyyy-MM-dd") + "|Habits]]"</code></center></td>
    </tr>
</table>

# ```dataview
LIST WITHOUT ID "Total Data Points: " + (length(rows.file.link)-1) WHERE contains(file.folder, this.file.folder) GROUP BY true
# ```

![[🎛️ Habits Dashboard#Consumption]]
![[🎛️ Habits Dashboard#Exertion]]
![[🎛️ Habits Dashboard#Other]]

```

# Habits
Todays Habit Tracker: `="[[" + "Habits/Habits - " + dateformat(date(today), "yyyy-MM-dd") + "]]"`
```dataview
LIST WITHOUT ID "Total Data Points: " + (length(rows.file.link)-1) WHERE contains(file.folder, this.file.folder) GROUP BY true
```
## Consumption
### Alcohol
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Alcohol)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Alcohol, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Red",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Ate Out?
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.AteOut)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.AteOut, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Red",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Caffeine
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Caffeine)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Caffeine, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Green",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Protein
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Protein)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Protein, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Pink",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```

### Sabzi
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Sabzi)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Sabzi, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Green",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Strict Diet?
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.StrictDiet)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.StrictDiet, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Blue",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Supplements
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Supplements)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Supplements, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Green",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
## Exertion
### Biking
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Bike)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Bike, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Pink",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Grips
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Grips)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Grips, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Pedurple",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### MMA/Grappling
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Grappling)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Grappling, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Pedurple",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### MMA/Striking
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Striking)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Striking, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Pedurple",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Push Ups
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.PushUps)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Pushups, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "OrangeToRed",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Pull Ups
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.PullUps)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.PullUps, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "OrangeToRed",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Running
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Run)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Run, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Orange",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
### Yoga
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Yoga)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Yoga, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Blue",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```
## Other
### Office
```dataviewjs
const calendarData = {
    // year: 2022,  // (optional) defaults to current year
    showCurrentDayBorder: true, // (optional) defaults to true
    // defaultEntryIntensity: 4,   // (optional) defaults to 4
    // intensityScaleStart: 10,    // (optional) defaults to lowest value passed to entries.intensity
    // intensityScaleEnd: 100,     // (optional) defaults to highest value passed to entries.intensity
    entries: [],                // (required) populated in the DataviewJS loop below
}

for (let page of dv.pages('"Habits"').where(p => p.Office)) {
    calendarData.entries.push({
        date: page.file.name.slice(-10),     // (required) Format YYYY-MM-DD
        intensity: page.Office, // (required) the data you want to track, will map color intensities automatically
        // content: "🏋️",           // (optional) Add text to the date cell
        color: "Green",          // (optional) Reference from *calendarData.colors*. If no color is supplied; colors[0] is used
    })
}

renderHeatmapCalendar(this.container, calendarData)
```

