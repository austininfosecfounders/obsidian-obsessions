<%*
const todayDate = tp.date.now("YYYY-MM-DD"); 

let pageName = `Habits - ${todayDate}`;
let pagePath = `Habits/${pageName}`;
 
// Check if the file already exists
if (tp.file.exists(pagePath)) {
    // If the file exists, delete the temporary untitled file we just created and jump to existing.
    // await tp.file.move("/dev/null");
    console.log("habit file exists, opening ${pagePath}");
    await app.workspace.openLinkText(pagePath, '/', false);
} else {
    console.log("habit file doesn't exist, creating and renaming");
    // If the file doesn't exist, set the current file's name to the desired format
    setTimeout(() => {
        tp.file.rename(pageName);
    }, 200);
} %>
# Consumption
Alcohol:: 
AteOut:: 
Caffeine:: 
Protein:: 
Sabzi:: 
StrictDiet:: 
Supplements:: 
# Exertion
Bike:: 
Grappling:: 
Grips:: 
PushUps:: 
PullUps:: 
Run::  
Striking:: 
Yoga:: 
# Other
Office:: 
