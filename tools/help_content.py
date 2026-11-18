"""Content of the Yaaddi help center. One entry per article; build_help.py turns them into pages.

Every instruction here was checked against the app's own screens and text (Settings, Learn menus,
Library, exams, backup) and, for the web build, in the running app. Keep it that way: when the app
changes, change the matching article and bump its `updated` date.

Fields
  slug      URL folder: /help/<slug>/
  category  one of CATEGORIES
  title     the H1 and the base of the page title: a task or a question people would type into a search box
  summary   the short answer, shown first (also used as the meta description when it fits)
  steps     optional numbered steps: (html, image key or None)
  sections  optional extra sections: (heading, html)
  notes     optional "Good to know" bullets (html)
  faq       optional (question, answer html) pairs
  related   slugs of related articles
  images    image key -> (file in assets/img/help/, alt text)
  updated   ISO date of the last check against the app
"""

CATEGORIES = [
    ("get-started", "Get started", "Install, import or create the courses you study."),
    ("study", "Study", "How lessons, questions, reviews and exams work."),
    ("progress", "Progress", "Streaks, Coins and your stats."),
    ("settings", "Settings", "Make Yaaddi look, sound and remind you the way you like."),
    ("your-data", "Your data", "Backups, updates, offline use and privacy."),
]

PLAY = "https://play.google.com/store/apps/details?id=com.yaaddi.app"

ARTICLES = [
    # ------------------------------------------------------------------ Get started
    {
        "slug": "is-yaaddi-free",
        "category": "get-started",
        "title": "Is Yaaddi free?",
        "summary": "Yes. Yaaddi is free on Google Play, has no ads and needs no account. The courses in the Course Library are free too.",
        "sections": [
            ("What you get", "<ul><li>The Yaaddi app, free to download from <a href=\"" + PLAY + "\" rel=\"noopener\">Google Play</a></li><li>Every course in the in-app Course Library, which you can also browse on <a href=\"https://courses.yaaddi.com/\" rel=\"noopener\">courses.yaaddi.com</a></li><li>No ads and no account to create</li></ul>"),
        ],
        "notes": [
            "Yaaddi runs on Android. It is available from Google Play.",
            "Your courses and progress are stored on your phone. See <a href=\"../privacy-and-your-data/\">Where does Yaaddi store my data?</a>",
        ],
        "faq": [
            ("Who makes Yaaddi?", "Yaaddi is made by Mohammad Reza Mahdiani, a software engineer. You can reach the team at <a href=\"mailto:support@yaaddi.com\">support@yaaddi.com</a>."),
        ],
        "related": ["install-a-course", "use-offline", "privacy-and-your-data"],
        "images": {},
        "updated": "2026-11-18",
    },
    {
        "slug": "install-a-course",
        "category": "get-started",
        "title": "How to install a course in Yaaddi",
        "summary": "Open the Course Library from the Learn tab, find a course and tap Install. The course downloads to your phone and appears on the Learn tab, ready to study offline.",
        "steps": [
            ("Open the <strong>Learn</strong> tab and tap the <strong>Course Library</strong> button (the shop icon at the top right). On a fresh install you can also tap <strong>Browse course library</strong>.", "library"),
            ("Scroll the list or type in <strong>Search courses</strong>. Tap a tag, such as <em>python</em> or <em>ai</em>, to filter. <strong>Read more</strong> shows the full description and what is inside.", None),
            ("Tap <strong>Install</strong> on the course you want. The app shows <em>Downloading</em>, <em>Reading course</em> and <em>Saving course</em>, then the button changes to <strong>Installed</strong>.", None),
            ("Go back to the <strong>Learn</strong> tab. Tap the course card to open its map and start with the first deck.", "learn-courses"),
        ],
        "notes": [
            "The library needs an internet connection. Once a course is installed you can study it without one.",
            "Courses come from a public GitHub repository run by Yaaddi. The app does not send an account or any personal identifier when it downloads them.",
            "Installing a course does not change courses you already have. Your progress is stored on your phone.",
            "You can also browse every course, with its full list of decks, on <a href=\"https://courses.yaaddi.com/\" rel=\"noopener\">courses.yaaddi.com</a> before you install.",
        ],
        "faq": [
            ("Why is the Course Library empty or not loading?", "The library is downloaded when you open it, so it needs a connection. Check your internet, then open it again. The message <em>Could not load the course library</em> means the download failed."),
            ("Do courses cost anything?", "No. Yaaddi and all the courses in the library are free."),
        ],
        "related": ["import-a-course", "update-a-course", "use-offline"],
        "images": {
            "library": ("library.webp", "Yaaddi's Course Library listing courses such as AI at Work, each with a description, tags and an Install button"),
            "learn-courses": ("learn-courses.webp", "The Learn tab in Yaaddi showing an installed Python Basics course with its progress bar"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "import-a-course",
        "category": "get-started",
        "title": "How to import a course file into Yaaddi",
        "summary": "On the Learn tab, tap the three-dot menu, choose Import a course and pick a course file. Yaaddi accepts a course .json file or a course .zip file.",
        "steps": [
            ("Open the <strong>Learn</strong> tab and tap the three-dot button at the top right.", "more-actions-menu"),
            ("Choose <strong>Import a course</strong>.", None),
            ("Pick the <code>.json</code> or <code>.zip</code> file from your phone. The app shows <em>Validating course</em>, then adds the course to the Learn tab.", None),
        ],
        "notes": [
            "A course that is not valid fails with a message that names the card and the reason, so a mistake in a hand-made file is easy to find.",
            "The ZIP form can include pictures and audio. A JSON file can carry the same content as text.",
            "To change a course you already imported, use <strong>Update from file</strong> in the course's menu. See <a href=\"../update-a-course/\">How to update a course</a>.",
            "Courses are built from plain CSV files. The public <a href=\"https://github.com/yaaddi-courses\" rel=\"noopener\">yaaddi-courses</a> organization on GitHub holds the course template and authoring guide.",
        ],
        "faq": [
            ("Which file types can I import?", "A course <code>.json</code> file or a course <code>.zip</code> file. Both work from the same <strong>Import a course</strong> option."),
            ("Does importing a course upload it anywhere?", "No. The file is read on your phone and stored in the app's local database."),
        ],
        "related": ["create-a-course", "install-a-course", "update-a-course", "export-a-course"],
        "images": {
            "more-actions-menu": ("more-actions-menu.webp", "The three-dot menu on Yaaddi's Learn tab with Create a course, Import a course, New group, Sort courses, Create backup and Restore backup"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "create-a-course",
        "category": "get-started",
        "title": "How to create your own course in Yaaddi",
        "summary": "Tap the three-dot menu on the Learn tab, choose Create a course, give it a title and save it. Then add decks and manage their cards.",
        "steps": [
            ("On the <strong>Learn</strong> tab, tap the three-dot button and choose <strong>Create a course</strong>.", "create-course"),
            ("Enter a <strong>Title</strong>. It is the only required field. Optionally add a cover image, a description, a color, an icon and tags.", None),
            ("Tap <strong>Save</strong>. You must save once before you can add decks.", None),
            ("Under <strong>Decks</strong>, type a name in <em>New deck name</em> and add it. Repeat for each deck. Decks appear in order on the course map, and an optional <em>Section</em> label groups consecutive decks.", None),
            ("Tap <strong>Manage cards in this course</strong> to add and edit the questions in each deck.", None),
        ],
        "notes": [
            "Use the up and down arrows next to a deck to reorder it. Deleting a deck also deletes its cards, and the app asks you to confirm.",
            "If you leave without saving, Yaaddi asks whether to discard your changes.",
            "Open <strong>Edit course</strong> in the course's menu at any time to change the title, color, icon or decks.",
            "For a long course, importing a ready-made file is faster than typing every card. See <a href=\"../import-a-course/\">How to import a course file</a>.",
        ],
        "faq": [
            ("Can I add pictures to my own course?", "Yes. You can add a cover image to the course and images to decks and sections."),
            ("Can I share a course I made?", "Yes. Export it from the course menu. See <a href=\"../export-a-course/\">How to share a course</a>."),
        ],
        "related": ["import-a-course", "export-a-course", "question-types", "organize-courses"],
        "images": {
            "create-course": ("create-course.webp", "Yaaddi's New course screen with fields for cover image, title, description and color, and a Save button"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "organize-courses",
        "category": "get-started",
        "title": "How to organize, sort and delete courses in Yaaddi",
        "summary": "Use the three-dot menu on the Learn tab to make groups and sort courses, and the menu on each course card to move it to a group, edit it or delete it.",
        "steps": [
            ("To make a folder, open the three-dot menu on the <strong>Learn</strong> tab and choose <strong>New group</strong>. Give it a name and tap <strong>Create</strong>.", "more-actions-menu"),
            ("To put a course in a group, tap the three dots on the course card and choose <strong>Move to group</strong>.", "course-card-menu"),
            ("To change the order, choose <strong>Sort courses</strong> in the three-dot menu. A custom order lets you drag courses where you want them.", None),
            ("To find a course quickly, type in the <strong>Find a course</strong> box at the top of the Learn tab.", None),
            ("To remove a course, tap the three dots on its card and choose <strong>Delete</strong>.", None),
        ],
        "notes": [
            "Deleting a course removes its cards and your progress on them from this phone. If you might want it back, create a backup first. See <a href=\"../backup-and-restore/\">How to back up Yaaddi</a>.",
            "A course from the library can be installed again at any time, but your old progress will not come back unless you restore a backup.",
        ],
        "faq": [
            ("Can I put a group inside another group?", "Yes. Groups can contain subgroups."),
        ],
        "related": ["backup-and-restore", "install-a-course", "create-a-course"],
        "images": {
            "more-actions-menu": ("more-actions-menu.webp", "The three-dot menu on Yaaddi's Learn tab with New group and Sort courses highlighted among the options"),
            "course-card-menu": ("course-card-menu.webp", "The menu of a course card in Yaaddi with Manage cards, Edit course, Update from file, Export, Move to group and Delete"),
        },
        "updated": "2026-11-18",
    },
    # ------------------------------------------------------------------ Study
    {
        "slug": "skip-what-you-know",
        "category": "study",
        "title": "How to skip what you already know in a Yaaddi course",
        "summary": "Open the course map and tap the lightning button, labeled \"What do you know?\". Answer a few questions for about five minutes and Yaaddi marks the decks you know so you only study what is new.",
        "steps": [
            ("Open a course from the <strong>Learn</strong> tab to see its map.", "course-map"),
            ("Tap the lightning-bolt button in the course banner (its label is <em>What do you know? Skip what you already know</em>), then tap <strong>Start</strong>.", "placement"),
            ("Answer the questions. Tap <strong>I don't know</strong> instead of guessing. You can stop at any time.", None),
            ("When the check ends, tap <strong>Skip what I know</strong> to save the result, or <strong>Start from the beginning</strong> to ignore it.", None),
        ],
        "sections": [
            ("What the check does", "<p>It samples questions from the first decks. If you answer correctly, it tries later decks with a bigger step. If a step is too far, it goes back and uses a smaller one. The decks you know are marked as known and come back for a quick review in a few days, so nothing you skip is forgotten.</p>"),
        ],
        "notes": [
            "The check stops once it has skipped enough for now. You can take it again whenever you like.",
            "<strong>Redo this round</strong> undoes the last round of the check.",
            "You can also test out of a single deck with <strong>Test out of this deck</strong> from that deck's menu.",
            "A course needs enough questions in its early decks to offer the check. Otherwise the app says it does not have enough yet.",
        ],
        "faq": [
        ],
        "related": ["take-an-exam", "change-spaced-repetition-algorithm", "question-types"],
        "images": {
            "course-map": ("course-map.webp", "A course map in Yaaddi with a lightning button and a Test yourself button under the course banner"),
            "placement": ("placement.webp", "Yaaddi's What do you know? screen explaining the quick check and a green Start button"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "question-types",
        "category": "study",
        "title": "Question types in Yaaddi",
        "summary": "Yaaddi has 20 question types. You answer by choosing, ordering, matching, sorting, typing or filling in a blank, instead of flipping a card and grading yourself.",
        "sections": [
            ("The 20 types", "<ul class=\"cols\"><li>Multiple choice</li><li>True or false</li><li>Put in order</li><li>Type the answer</li><li>Type a short answer</li><li>Type the number</li><li>Fill in the blank (tap)</li><li>Select all that apply</li><li>Match the pairs</li><li>Pick the icon</li><li>Fill in the code or command</li><li>Predict the output</li><li>Label the diagram</li><li>Sort into groups</li><li>Spot the error</li><li>Listening</li><li>Reading passage</li><li>Cloze passage</li><li>Media card</li><li>Preview</li></ul>"),
            ("How answering works", "<p>You answer, then tap <strong>Check</strong> where the card has one. The result appears at once, with an encouraging message and, when the course author wrote one, <strong>See explanation</strong>. Tap <strong>Continue</strong> for the next card.</p>"),
            ("Where practice comes from", "<p>Because every question has a right answer, Yaaddi grades it for you. It records only whether you were correct, and the spaced-repetition schedule uses that. A wrong answer is followed by related practice cards. See <a href=\"../practice-cards/\">What practice cards are</a>.</p>"),
        ],
        "notes": [
            "Preview cards introduce an idea before you are asked about it.",
            "Listening cards play audio. If you cannot listen right now, open <strong>Course settings</strong> in a language course and use <strong>Skip listening cards</strong> to skip them for 3 hours, today or this session.",
            "Cards that need typing are kept to a minimum on purpose, so you can study on a phone without a keyboard getting in the way.",
        ],
        "faq": [
            ("What if a question or its answer looks wrong?", "Report it from the card. See <a href=\"../report-a-problem/\">How to report a mistake in a card</a>."),
            ("Can I skip one card?", "Yes. In a lesson, open the three-dot menu and choose <strong>Skip this card for now</strong>."),
        ],
        "related": ["practice-cards", "report-a-problem", "change-spaced-repetition-algorithm"],
        "images": {},
        "updated": "2026-11-18",
    },
    {
        "slug": "practice-cards",
        "category": "study",
        "title": "What practice cards are and how to change them in Yaaddi",
        "summary": "Practice cards are extra questions linked to a main card. Yaaddi shows them when you learn a card for the first time and right after a wrong answer. You can tune both in Settings → Advanced learning options.",
        "steps": [
            ("Open the <strong>Settings</strong> tab and tap <strong>Advanced learning options</strong>.", "settings-advanced"),
            ("Under <strong>Practice cards for new material</strong>, choose <strong>All</strong>, <strong>Adaptive</strong> or <strong>None</strong>. This only affects the first time you learn a card.", None),
            ("With <strong>Adaptive</strong>, set <strong>Fade after</strong>: how many correct answers in a row on a card's practice exercises before the rest fade out.", None),
            ("Under <strong>Practice cards on a wrong answer</strong>, choose how many of a missed card's practice cards are asked right after it: all of them, or a fixed number.", None),
            ("Turn on <strong>All cards in spaced repetition</strong> if you want practice cards to be scheduled for review too, each on its own schedule.", None),
        ],
        "notes": [
            "Main cards are always scheduled for review. Practice cards are scheduled only if you turn on <strong>All cards in spaced repetition</strong>.",
            "Cards you are reviewing again later always show practice only after a wrong answer, whatever the new-material setting says.",
            "The defaults suit most people. Change one setting at a time so you can tell what helps.",
        ],
        "faq": [
            ("What does \"Custom\" do?", "<strong>Custom</strong> lets you set the exact number of practice cards to show up front, instead of all or adaptive."),
        ],
        "related": ["question-types", "change-spaced-repetition-algorithm"],
        "images": {
            "settings-advanced": ("settings-advanced.webp", "Yaaddi's Settings with Advanced learning options expanded to show the Spaced repetition algorithm choices"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "change-spaced-repetition-algorithm",
        "category": "study",
        "title": "How to change the spaced-repetition algorithm in Yaaddi",
        "summary": "Go to Settings, open Advanced learning options and pick SM-2, Fibonacci, FSRS, ACT-R or HLR under Spaced repetition. Your progress is kept; cards become due again so they can pick up the new schedule.",
        "steps": [
            ("Open the <strong>Settings</strong> tab and tap <strong>Advanced learning options</strong>.", "settings-advanced"),
            ("Under <strong>Spaced repetition</strong>, tap the algorithm you want: <strong>SM-2 (Classic)</strong>, <strong>Fibonacci</strong>, <strong>FSRS v5</strong>, <strong>ACT-R</strong> or <strong>HLR</strong>.", None),
            ("Read the prompt <em>Switch scheduling algorithm?</em> and tap <strong>Switch</strong> to confirm, or <strong>Cancel</strong> to keep the current one.", None),
        ],
        "sections": [
            ("The five algorithms", "<dl><dt>SM-2 (Classic)</dt><dd>The classic SuperMemo 2 method used by Anki. Each card has an ease factor, and the gap between reviews multiplies as you keep answering correctly.</dd><dt>Fibonacci</dt><dd>Review gaps follow the Fibonacci sequence. Simple and predictable.</dd><dt>FSRS</dt><dd>Models how memory fades, using each card's stability and difficulty. The newest of the five, and the one Anki now offers as an alternative to SM-2. Yaaddi's version is inspired by FSRS and adapted for right-or-wrong answers.</dd><dt>ACT-R</dt><dd>Based on a cognitive model of memory decay, where gaps grow with how often you have practiced a card.</dd><dt>HLR</dt><dd>Half-Life Regression, the approach Settles and Meeder published and Duolingo uses. Each card has an estimated memory half-life that grows by about 23% after a correct answer and shrinks by about 29% after a wrong one.</dd></dl>"),
            ("Which one should I choose?", "<p>The default works well for most people, and there is no setting that is right for everyone. Yaaddi grades answers as simply correct or incorrect, with no \"hard\" or \"easy\" buttons, so all five are adapted to that. If you have no strong reason to switch, keep the default. If you want to experiment, change one thing and study for a few weeks before you judge it.</p>"),
        ],
        "notes": [
            "Switching never deletes anything. Every card keeps the progress you have made, but becomes due for review right away so it can pick up the new algorithm's schedule. Expect a larger first review session after a switch.",
            "Your Coins, streaks and review history are not affected.",
            "<strong>New day starts at</strong>, in the same section, sets when a card scheduled for \"tomorrow\" becomes due. The default is 2:00 a.m.",
            "If a switch fails, the app tells you nothing was changed. Check that the phone has free storage and try again.",
        ],
        "faq": [
            ("What is spaced repetition?", "A study method that shows you a fact again just before you would forget it. Correct answers push the next review further away; wrong answers bring it closer."),
            ("Does Yaaddi have \"Again, Hard, Good, Easy\" buttons like Anki?", "No. Yaaddi questions have one right answer, so the app grades them for you as correct or incorrect."),
        ],
        "related": ["practice-cards", "question-types", "streaks-freezes-coins"],
        "images": {
            "settings-advanced": ("settings-advanced.webp", "Yaaddi's Settings with Advanced learning options open and the SM-2, Fibonacci and FSRS options under Spaced repetition"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "take-an-exam",
        "category": "study",
        "title": "How to take a practice exam in Yaaddi",
        "summary": "Open a course and tap Test yourself. Choose what to be tested on, the number of questions and an optional timer. You see your score, a per-deck breakdown and every correct answer only after you submit.",
        "steps": [
            ("Open a course from the <strong>Learn</strong> tab and tap <strong>Test yourself</strong>.", "course-map"),
            ("Pick the exam. A course can offer an <strong>Official exam format</strong> (a fixed number of questions, time limit and pass mark), numbered exams, or a <strong>Random mix</strong>.", None),
            ("Under <strong>What should you be tested on?</strong>, choose <strong>Whole course</strong>, <strong>Decks I've studied</strong> or <strong>Choose decks</strong>.", None),
            ("For a practice exam, set the number of questions and the time limit, or turn the timer off. Tap <strong>Start exam</strong>.", None),
            ("Answer one question at a time. Use <strong>Flag for review</strong> to mark a question and <strong>Questions</strong> to jump around. Tap <strong>Submit exam</strong> when you are done.", None),
        ],
        "sections": [
            ("What you see afterwards", "<p>The results screen shows pass or not passed, your score, a breakdown by deck, and a review of every question with the right answer and the author's explanation. <strong>Practice my mistakes</strong> starts an untimed exam made from the questions you got wrong.</p>"),
        ],
        "notes": [
            "During an exam there is no feedback: no colors, sounds or explanations, so it feels like the real thing. You can change answers until you submit.",
            "The exam is saved as you go, and the clock does not stop if you close the app. Reopen Test yourself to <strong>Resume exam</strong> or <strong>Discard it</strong>.",
            "Exams use multiple-choice and true-or-false questions, and they never change your spaced-repetition schedule.",
            "Each correct answer earns one Coin when the results are shown. Nothing is taken away for a wrong or blank answer.",
            "Passing the whole course at full length earns a certificate you can share. It says it is a practice exam inside Yaaddi and <strong>is not an official certificate</strong>, which matters for courses such as driving or citizenship tests.",
        ],
        "faq": [
            ("Why is Test yourself missing or unavailable?", "A course needs multiple-choice or true-or-false questions to build an exam. Otherwise the app says <em>This course has no multiple-choice or true/false questions to build an exam from</em>."),
            ("Can I report a bad question?", "Yes. Every question has <strong>Report a problem with this question</strong>, during the exam and in the results review."),
        ],
        "related": ["skip-what-you-know", "report-a-problem", "streaks-freezes-coins"],
        "images": {
            "course-map": ("course-map.webp", "A Yaaddi course map with the Test yourself button under the course banner"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "report-a-problem",
        "category": "study",
        "title": "How to report a mistake in a Yaaddi card",
        "summary": "While studying, tap the three-dot menu and choose Report a problem. Pick a reason, add a note, and Yaaddi opens your email app with the report ready to send. Nothing is sent until you press send.",
        "steps": [
            ("In a lesson, tap the three-dot button at the top right.", None),
            ("Choose <strong>Report a problem</strong>.", None),
            ("Pick a reason: <em>The correct answer is wrong</em>, <em>Typo or unclear wording</em>, <em>Inappropriate content</em>, <em>Image or audio does not work</em> or <em>Something else</em>. Add details if you like.", None),
            ("Tap <strong>Continue</strong>. Your email app opens with the message filled in. Review it and press send.", None),
        ],
        "notes": [
            "The email goes to <a href=\"mailto:support@yaaddi.com\">support@yaaddi.com</a> and includes your note, the reason, the course name and version, the card ID and type, a short excerpt of the card text, and the app version and platform. You see all of it before you send.",
            "In an exam, use <strong>Report a problem with this question</strong> on the question or in the results review.",
            "If no email app opens, write to support@yaaddi.com and name the course and the card.",
        ],
        "faq": [
            ("What happens to my report?", "We use it to fix the card and to reply to you at the address you sent it from. A correction reaches you as an updated course version. See <a href=\"../update-a-course/\">How to update a course</a>."),
        ],
        "related": ["question-types", "take-an-exam", "update-a-course"],
        "images": {},
        "updated": "2026-11-18",
    },
    # ------------------------------------------------------------------ Progress
    {
        "slug": "streaks-freezes-coins",
        "category": "progress",
        "title": "How streaks, streak freezes and Coins work in Yaaddi",
        "summary": "Your streak counts the days in a row you studied. A streak freeze covers a missed day. Coins go up by one for every correct answer and are never taken away.",
        "sections": [
            ("Streak", "<p>Study at least once a day to keep your streak. Tap the flame at the top of the app to see your current streak. Miss a day and it restarts, unless a freeze or the weekly grace day covers it.</p><figure class=\"help-shot\"><img src=\"../../assets/img/help/streak-info.webp\" width=\"480\" height=\"1039\" loading=\"lazy\" decoding=\"async\" alt=\"Yaaddi's streak explanation dialog: days in a row you studied, restarting if you miss a day unless a streak freeze covers it\"></figure>"),
            ("Streak freezes", "<ul><li>You earn one every 7 days in a row, and you keep at most 2.</li><li>A freeze is spent automatically to cover a missed day. You do not need to do anything.</li><li>Every new learner gets one freeze on their first session.</li><li>One missed day is also forgiven for free once every 7 days, before any freeze is used.</li></ul>"),
            ("Streak repair", "<p>If a streak of at least 3 days ends, the app offers to bring it back: answer 15 questions that same day and it is restored. The offer expires at the end of that day.</p>"),
            ("Coins", "<p>You earn 1 Coin for every correct answer. A wrong answer, a missed day or a broken streak never lowers your Coins. Streak milestones add a one-time bonus the first time you reach them: 10 Coins at 7 days, 30 at 30 days, 100 at 100 days and 300 at 365 days. Each correct exam answer also earns a Coin.</p>"),
        ],
        "notes": [
            "Your streak and Coins are stored on your phone. Create a backup before you change phones so you do not lose them. See <a href=\"../backup-and-restore/\">How to back up Yaaddi</a>.",
            "The Stats tab shows your longest streak, total days studied and how many freezes you have saved, earned and used.",
        ],
        "faq": [
            ("Do I lose Coins if I miss a day?", "No. Coins never go down. Only the streak counter restarts."),
            ("Why did my streak survive a missed day?", "A streak freeze or the weekly grace day covered it. The app tells you with a <em>Streak saved!</em> message."),
            ("What time does my day end?", "By default a new study day starts at 2:00 a.m., so late-night study still counts toward the day you started it. <strong>Settings → Advanced learning options → New day starts at</strong> changes that time."),
        ],
        "related": ["see-your-progress", "study-reminders", "backup-and-restore"],
        "images": {
            "streak-info": ("streak-info.webp", "Yaaddi's streak explanation: days in a row you studied, restarting if you miss a day unless a streak freeze covers it"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "see-your-progress",
        "category": "progress",
        "title": "Where to see your progress and stats in Yaaddi",
        "summary": "Open the Stats tab. It shows cards answered, accuracy, total Coins, days studied, your streaks and freezes, and charts of your progress over time. Each course has its own stats too.",
        "steps": [
            ("Open the <strong>Stats</strong> tab at the bottom of the app.", "stats"),
            ("Switch between <strong>All time</strong> and <strong>This week</strong> at the top of the summary.", None),
            ("Scroll to <strong>Progress over time</strong> and choose 7 days, 30 days, 90 days or All. Tap a chart to see a single day.", None),
            ("Use the course dropdown to see the stats of one course, including its exams.", None),
            ("Tap <strong>Share progress</strong> to send a picture of your progress and a link to the app through any app you choose.", None),
        ],
        "notes": [
            "Stats count lesson answers. Exam answers appear in the Exams section instead and stay out of your accuracy.",
            "On the Learn tab, the number of cards due today and the <strong>Study</strong> button show what to review next.",
            "Everything is calculated on your phone. Sharing progress sends nothing by itself: you choose where the picture goes.",
        ],
        "faq": [
            ("Why are my stats empty?", "They fill in after you answer your first cards. Install a course from the library and study a deck."),
        ],
        "related": ["streaks-freezes-coins", "take-an-exam", "backup-and-restore"],
        "images": {
            "stats": ("stats.webp", "Yaaddi's Stats tab with a Share progress button, an All time and This week switch, and cards answered, accuracy, total Coins and days studied"),
        },
        "updated": "2026-11-18",
    },
    # ------------------------------------------------------------------ Settings
    {
        "slug": "dark-mode-text-size-and-sound",
        "category": "settings",
        "title": "How to change dark mode, text size and sounds in Yaaddi",
        "summary": "Open the Settings tab. Under Look and sound, choose System, Light or Dark for Appearance, use the minus and plus buttons for Text size, and switch Sound effects and Animations on or off.",
        "steps": [
            ("Open the <strong>Settings</strong> tab.", "settings"),
            ("Under <strong>Appearance</strong>, choose <strong>System</strong> to follow your phone, or <strong>Light</strong> or <strong>Dark</strong>.", None),
            ("Under <strong>Text size</strong>, tap the minus or plus button to make text smaller or larger across the app. 100% is the default.", None),
            ("Switch <strong>Sound effects</strong> on or off to play or mute the sound on correct and incorrect answers.", None),
            ("Switch <strong>Animations</strong> off to turn off confetti, bounce effects and modal entrance animations.", None),
        ],
        "notes": [
            "In language courses, <strong>Read cards aloud</strong> reads the language being taught automatically when a card appears. The voice is your phone's own text-to-speech engine.",
            "<strong>App language</strong> follows your phone. To change it, tap <strong>Open phone settings</strong> and choose Language for Yaaddi.",
        ],
        "faq": [
            ("Does Yaaddi have a dark mode?", "Yes. Choose <strong>Dark</strong> under Appearance, or leave it on <strong>System</strong> so it follows your phone."),
        ],
        "related": ["study-reminders", "practice-cards"],
        "images": {
            "settings": ("settings.webp", "Yaaddi's Settings tab with Appearance set to System, Light or Dark, and switches for Sound effects, Text size and Animations"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "study-reminders",
        "category": "settings",
        "title": "How to set a daily study reminder in Yaaddi",
        "summary": "In Settings, under Reminders, switch on Daily study reminder and choose a time. Yaaddi nudges you at that time on days you have not studied yet.",
        "steps": [
            ("Open the <strong>Settings</strong> tab and find <strong>Reminders</strong>.", None),
            ("Switch on <strong>Daily study reminder</strong>. If your phone asks to allow notifications, allow them.", None),
            ("Set the <strong>Reminder time</strong>. Tap <strong>Suggest a time from my history</strong> to let the app pick a time you usually study.", None),
        ],
        "notes": [
            "The reminder may arrive a few minutes late, and it is skipped on days you have already studied.",
            "If you stay away, reminders continue for up to a week and then stop. Opening the app re-plans them.",
            "Reminders are scheduled on your phone. Nothing is sent to a server and the app uses no push service.",
            "If you see <em>Notifications are blocked</em>, allow notifications for Yaaddi in your phone's settings.",
            "Suggest a time needs some study history first. Before that, the app tells you there is not enough yet.",
        ],
        "faq": [
            ("Why am I not getting reminders?", "Check that the switch is on, that notifications are allowed for Yaaddi in your phone's settings, and that your phone is not stopping the app in the background with battery saving."),
            ("Does the reminder know how many cards are due?", "Yes. When cards are due, the notification says how many; otherwise it shows a short encouragement."),
        ],
        "related": ["streaks-freezes-coins", "dark-mode-text-size-and-sound"],
        "images": {},
        "updated": "2026-11-18",
    },
    # ------------------------------------------------------------------ Your data
    {
        "slug": "backup-and-restore",
        "category": "your-data",
        "title": "How to back up Yaaddi and move it to a new phone",
        "summary": "On the Learn tab, tap the three-dot menu and choose Create backup. Save the file somewhere safe. On the new phone, open the same menu, choose Restore backup and pick the file.",
        "steps": [
            ("On the <strong>Learn</strong> tab, tap the three-dot button and choose <strong>Create backup</strong>. This option appears once you have at least one course.", "more-actions-menu"),
            ("Choose where to save or share the file, such as your cloud drive or an email to yourself.", None),
            ("On the new phone, install Yaaddi, open the same menu and choose <strong>Restore backup</strong>.", None),
            ("Pick the backup file and confirm. Yaaddi shows <em>Restore complete</em> when it has finished.", None),
        ],
        "notes": [
            "A backup holds your courses, progress, streak, Coins and settings.",
            "<strong>Restoring replaces</strong> the courses, stats and settings on the phone with what is in the file. Restore onto a new phone, or after a backup you are sure about.",
            "Yaaddi keeps no copy of your data, and Android's automatic cloud backup is turned off for the app. The file you create is the backup, so keep it somewhere you can reach.",
            "A backup over 100 MB cannot be restored later, and the app warns you. Delete courses you no longer need or share them one by one.",
            "Uninstalling the app or clearing its storage deletes your data from the phone.",
        ],
        "faq": [
            ("Where is the backup saved?", "Wherever you choose when you create it. You are responsible for that copy."),
            ("Can I move only one course?", "Yes. Use <strong>Export</strong> from the course menu to share a single course without your progress. See <a href=\"../export-a-course/\">How to share a course</a>."),
            ("Why is Create backup missing?", "It needs at least one course. Restore backup is always available, even on a fresh install."),
        ],
        "related": ["export-a-course", "organize-courses", "privacy-and-your-data"],
        "images": {
            "more-actions-menu": ("more-actions-menu.webp", "The Learn tab's three-dot menu in Yaaddi, with Create backup and Restore backup near the bottom"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "update-a-course",
        "category": "your-data",
        "title": "How to update a course in Yaaddi",
        "summary": "Open the Course Library, find Installed courses and tap Check for updates, then Update. Progress on cards that did not change is kept.",
        "steps": [
            ("Open the <strong>Course Library</strong> from the <strong>Learn</strong> tab.", "library"),
            ("Under <strong>Installed courses</strong>, tap <strong>Check for updates</strong>. A course with news shows <strong>Update available</strong>.", None),
            ("Tap <strong>Update</strong>. When it finishes you see <em>Course updated</em>: new content is in, and your review progress for anything unchanged was kept.", None),
        ],
        "notes": [
            "When you open an installed course, Yaaddi also checks for a newer version, at most once a day per course. A banner says <em>An update is available for this course</em> with a <strong>View</strong> button.",
            "If an update removes cards you have already studied, the app tells you how many and asks whether to continue, because their progress would be lost.",
            "For a course you imported from a file, use <strong>Update from file</strong> in the course's menu instead.",
            "To update the Yaaddi app itself, use Google Play. A red dot on the Settings tab shows when a new version is available.",
        ],
        "faq": [
            ("Do I lose my progress when a course updates?", "Not for cards that stay in the course. Only cards the update removes lose their progress, and you are warned first."),
        ],
        "related": ["install-a-course", "import-a-course", "report-a-problem"],
        "images": {
            "library": ("library.webp", "Yaaddi's Course Library, where installed courses show a Check for updates button"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "export-a-course",
        "category": "your-data",
        "title": "How to share a course from Yaaddi",
        "summary": "Tap the three dots on a course card and choose Export. Yaaddi prepares a course file you can send to anyone. The shared file never includes your review progress.",
        "steps": [
            ("On the <strong>Learn</strong> tab, tap the three dots on the course card and choose <strong>Export</strong>.", "course-card-menu"),
            ("Choose <strong>Export</strong> to share the course as it is, or <strong>Export &amp; reset my progress</strong> to share it and also start the course over for yourself.", None),
            ("Pick the app or place to send the file.", None),
        ],
        "notes": [
            "The person receiving the file adds it with <strong>Import a course</strong>. See <a href=\"../import-a-course/\">How to import a course file</a>.",
            "Export shares a course. To keep your own progress safe, use a backup instead. See <a href=\"../backup-and-restore/\">How to back up Yaaddi</a>.",
        ],
        "faq": [
            ("Is my progress in the exported file?", "No. The shared file never includes your review progress."),
        ],
        "related": ["import-a-course", "backup-and-restore", "create-a-course"],
        "images": {
            "course-card-menu": ("course-card-menu.webp", "A Yaaddi course card menu with Manage cards, Edit course, Update from file, Export, Move to group and Delete"),
        },
        "updated": "2026-11-18",
    },
    {
        "slug": "use-offline",
        "category": "your-data",
        "title": "Does Yaaddi work offline?",
        "summary": "Yes. After a course is installed, you can study it, take exams and track progress without a connection. Only the Course Library and course and app updates need the internet.",
        "sections": [
            ("What works offline", "<ul><li>Studying any installed course and answering every question type</li><li>Spaced-repetition reviews and practice cards</li><li>Exams and certificates</li><li>Stats, streaks, Coins and settings</li><li>Creating, editing and importing courses from files on your phone</li><li>Reading the privacy policy and terms inside the app</li></ul>"),
            ("What needs a connection", "<ul><li>Opening the Course Library and installing a course</li><li>Checking for and installing course updates</li><li>Checking Google Play for a new version of the app</li><li>Pictures in an imported course that point to a web address</li></ul>"),
        ],
        "notes": [
            "Install the courses you want while you are online. Then Yaaddi works on a flight, a commute or anywhere with no signal.",
            "Reading aloud uses your phone's own text-to-speech engine, so it does not need a connection either.",
        ],
        "faq": [
            ("Do I need an account?", "No. There are no accounts. Your courses and progress are stored on your phone."),
        ],
        "related": ["install-a-course", "privacy-and-your-data", "update-a-course"],
        "images": {},
        "updated": "2026-11-18",
    },
    {
        "slug": "privacy-and-your-data",
        "category": "your-data",
        "title": "Where does Yaaddi store my data, and is it private?",
        "summary": "Your courses, cards, progress, streaks, Coins and settings stay in a database on your phone. Yaaddi has no accounts, no ads, and no analytics or crash-reporting tools, and it does not read advertising IDs.",
        "sections": [
            ("What stays on your phone", "<p>Everything you create or earn: courses, cards, review history, streaks, Coins, settings, and any cover images or audio you add. The developer never receives it. Uninstalling the app or clearing its storage deletes it.</p>"),
            ("What leaves your phone", "<ul><li><strong>Course Library and updates:</strong> the app downloads course lists and files from a public GitHub repository. GitHub sees your IP address and the files requested, as with any website. Yaaddi sends no identifier.</li><li><strong>App updates:</strong> on Android, the app asks Google Play whether a newer version exists.</li><li><strong>Report a problem:</strong> opens your email app with a message you can read before you send.</li><li><strong>Sharing:</strong> Share progress sends a picture only to the app you choose.</li></ul>"),
            ("Permissions", "<p>Notifications (optional, for study reminders) and photos (optional, for cover images). Files are read only through the system file picker. The app never asks for the camera or microphone.</p>"),
        ],
        "notes": [
            "This describes the Yaaddi app. For the full legal text, read the <a href=\"https://courses.yaaddi.com/privacy/\" rel=\"noopener\">Yaaddi privacy policy</a>.",
            "This website, yaaddi.com, uses optional Google Analytics only if you accept it. See <a href=\"../../privacy/\">Privacy and analytics</a>.",
            "Yaaddi is not directed at children under 13.",
        ],
        "faq": [
            ("Can you delete my data?", "We hold no personal data about you, so there is nothing to delete on our side. To remove everything, uninstall the app or clear its storage. If you emailed a report and want it deleted, write to support@yaaddi.com."),
        ],
        "related": ["backup-and-restore", "use-offline", "study-reminders"],
        "images": {},
        "updated": "2026-11-18",
    },
]

BY_SLUG = {a["slug"]: a for a in ARTICLES}
