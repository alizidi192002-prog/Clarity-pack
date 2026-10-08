"""Product catalogue for the product pin feeds (ext_products.py).

Each product gets a landing page at templates/<slug>.html (on the claimed site, so Pinterest
accepts the link) with a button to its Gumroad page. "titles" are rotated for re-posts so the
same image goes out again with a new title/description. Keep descriptions keyword-rich, no hashtags.
"""
G = "https://claritydigital8.gumroad.com/l/"
STORE = "https://claritydigital8.gumroad.com/"
IMG = "https://raw.githubusercontent.com/alizidi192002-prog/Clarity-pack/main/pack/pins/"

PRODUCTS = {
 "christmas": dict(
  slug="christmas-holiday-budget-planner", name="Christmas & Holiday Budget Planner", price="4.99", link=G + "skpgb", priority=True,
  images=["v3/pin_christmas_a.jpg", "v3/pin_christmas_b.jpg"],
  blurb="Enjoy the holidays without the January money shock. Set one total budget and track every gift, meal and decoration against it.",
  features=["Gift list: person, gift idea, budget, spent, bought and wrapped checkboxes", "Holiday expenses: food, decor, travel, cards, events", "Summary: planned, spent, left, and how many gifts are bought and wrapped", "Reuse it every year — Excel, Google Sheets and Numbers"],
  titles=[
   ("Christmas Budget Planner Spreadsheet – Gift List & Holiday Budget Template", "Track every gift, meal and decoration against one holiday budget, with bought and wrapped checkboxes. Christmas budget spreadsheet for Google Sheets and Excel."),
   ("How to Budget for Christmas Without Overspending", "Set one Christmas budget, give every person a number and see what's left as you shop. A simple holiday budget planner and gift list spreadsheet."),
   ("Christmas Gift List Template – Track Who You Buy For and What You Spend", "Gift list spreadsheet with budget per person, amount spent, bought and wrapped. Stay on budget this Christmas. Google Sheets and Excel."),
   ("Holiday Budget Spreadsheet: Gifts, Food, Decor and Travel in One Place", "Plan the whole holiday season: gifts, hosting, decorations and travel against one budget. Christmas planner spreadsheet, instant download."),
   ("Christmas Planner Printable & Digital – Holiday Budget Tracker", "A holiday budget tracker you can use on your phone or print. Gift list, holiday expenses and a summary of what's left. Christmas budget template."),
   ("Christmas on a Budget: The Gift Budget Spreadsheet That Saves January", "Avoid the January money shock with a Christmas budget planner: total budget, per-person gift budgets and spending tracker in Google Sheets."),
   ("Secret Santa & Family Gift Budget Tracker Spreadsheet", "Keep family gifts, Secret Santa and friends within budget. Christmas gift tracker with bought and wrapped checkboxes for Google Sheets and Excel."),
   ("Christmas Shopping List Spreadsheet – Budget Every Gift Before You Buy", "Write a budget for each person before you shop and track what you spend. Christmas shopping list and holiday budget planner template."),
   ("Holiday Gift Budget Planner – How Much to Spend on Each Person", "Give each person on your list a gift budget and watch your total. Holiday gift budget spreadsheet for Excel, Google Sheets and Numbers."),
   ("Christmas Budget Template for Families – Gifts, Meals and Decorations", "Family Christmas budget: gifts for kids, holiday meals and decor in one simple spreadsheet. Reuse it every year. Instant download."),
  ]),
 "budget2027": dict(
  slug="2027-budget-planner", name="2027 Budget Planner", price="6.99", link=G + "rtbasg", priority=True,
  images=["v3/pin_budget2027_a.jpg", "v3/pin_budget2027_b.jpg"],
  blurb="Plan your whole 2027 in one spreadsheet. Set your categories and monthly budget once, then track each month on its own tab — January to December.",
  features=["Setup tab: your income and up to 20 spending categories", "12 monthly tabs: budget vs actual, overspending turns red, % used per category", "Year overview: income, spending and savings for every month, your savings rate and a full-year total per category", "Works in Excel, Google Sheets and Numbers — example numbers included"],
  titles=[
   ("2027 Budget Planner Spreadsheet – Monthly & Yearly Budget Template", "12 monthly budget tabs, budget vs actual and a year overview with your savings rate. 2027 budget planner for Google Sheets and Excel."),
   ("Plan Your 2027 Budget: 12-Month Budget Planner with Savings Tracker", "Start 2027 with a plan: monthly budgets, spending tracker and a yearly overview of income, spending and savings. Instant download spreadsheet."),
   ("New Year Budget Planner 2027 – Budget Template for Beginners", "A beginner-friendly 2027 budget template: set your categories once, track every month and see your savings rate. Google Sheets and Excel."),
   ("2027 Monthly Budget Spreadsheet – Budget vs Actual, January to December", "Track budget vs actual for every month of 2027 with overspending flags and a year-end summary. Yearly budget planner spreadsheet."),
   ("Yearly Budget Planner 2027 – See Your Savings Rate Every Month", "See how much you save each month of 2027. Yearly budget overview, monthly tabs and category totals. Budget planner for Google Sheets."),
   ("2027 Money Goals: Budget Planner Spreadsheet to Start the Year Right", "Turn your 2027 money goals into a monthly plan. Budget planner with income, 20 categories, monthly tracking and annual summary."),
   ("Budget Planner 2027 Google Sheets – Simple Monthly Budget Template", "Simple 2027 monthly budget template for Google Sheets and Excel: plan, track and review your spending all year."),
   ("Digital Budget Planner 2027 – Track Spending and Savings All Year", "A digital 2027 budget planner: monthly spending tracker, budget vs actual and savings overview. Works on phone and computer."),
   ("2027 Household Budget Spreadsheet – Plan Bills, Groceries and Savings", "Household budget for 2027: plan bills, groceries and savings each month and see the full-year picture. Excel and Google Sheets template."),
   ("Start 2027 Debt-Free and Saving: Monthly Budget Planner Template", "Build a monthly budget for 2027 that leaves room for savings and debt payments. Budget planner spreadsheet with year overview."),
  ]),
 "bundle": dict(
  slug="complete-budget-planner-bundle", name="Complete Budget & Planner Bundle — 14 Spreadsheets", price="19.99", link=G + "zpdnkk", priority=True,
  images=["v3/pin_bundle_a.jpg", "v3/pin_bundle_b.jpg"],
  blurb="Every ClarityPaperCo spreadsheet in one download — over 70% less than buying them one by one.",
  features=["2027 budget, 50/30/20 budget and paycheck budget planners", "Debt payoff, savings & sinking funds, net worth and bill trackers", "Christmas, wedding, freelancer, small business and Meta Ads trackers", "Habit tracker and weekly meal planner — Excel, Google Sheets and Numbers"],
  titles=[
   ("Budget Planner Bundle – 14 Finance Spreadsheet Templates", "14 spreadsheets: 2027 budget, paycheck budget, debt payoff, savings, net worth, bills, wedding, Christmas and more. Google Sheets and Excel."),
   ("Every Budget Spreadsheet You Need in One Bundle", "Budget, debt payoff, savings, bills, Christmas and wedding planners in one download for less than the price of four. Personal finance templates."),
   ("Personal Finance Spreadsheet Bundle – Budget, Debt, Savings and More", "A complete personal finance toolkit: monthly budget, debt snowball, sinking funds, net worth and bill tracker spreadsheets."),
   ("Google Sheets Budget Templates Bundle – 14 Planners, One Price", "14 Google Sheets and Excel budget templates in one bundle: yearly budget, paycheck budget, savings goals, debt payoff and more."),
   ("Money Management Bundle: Budget Planner, Debt Tracker and Savings Tracker", "Manage all your money with one set of spreadsheets: budget planner, debt payoff tracker, savings and net worth trackers."),
   ("Budget Spreadsheet Bundle for Beginners – Start Budgeting Today", "Everything a beginner needs to start budgeting: 50/30/20 budget, paycheck budget, bill tracker and savings tracker in one bundle."),
   ("Financial Planner Bundle 2027 – 14 Excel & Google Sheets Templates", "Plan 2027 with 14 financial planner templates: budget, debt, savings, net worth, bills, Christmas, wedding and freelancer income."),
   ("Best Value Budget Templates: 14 Spreadsheets for 19.99€", "Get every budget template at over 70% off: budget planners, debt payoff, savings, bills and life-event planners. Instant download."),
   ("Family Budget Bundle – Bills, Groceries, Savings and Holiday Planners", "Family budget spreadsheets for bills, meal planning, savings goals, Christmas and big events. Google Sheets and Excel bundle."),
   ("Debt-Free & Saving Bundle – All the Budget Spreadsheets in One Download", "Pay off debt and grow savings with the complete budget spreadsheet bundle: debt snowball, sinking funds, net worth and monthly budget."),
  ]),
 "paycheck": dict(
  slug="paycheck-to-paycheck-budget-planner", name="Paycheck to Paycheck Budget Planner", price="4.99", link=G + "ljdxzm", priority=False,
  images=["v3/pin_paycheck_a.jpg", "v3/pin_paycheck_b.jpg"],
  blurb="Budget the way you actually get paid. Assign every bill to the paycheck that covers it and see exactly what's left from each one.",
  features=["Up to 5 paychecks a month (weekly, bi-weekly or monthly pay)", "Bill list with due day, amount and a 'paid from' dropdown", "Per-paycheck summary: income, bills, left over and still to pay — turns red if a paycheck can't cover its bills", "Mark bills as paid and the row turns green"],
  titles=[
   ("Paycheck to Paycheck Budget Spreadsheet – Biweekly Budget Template", "See which paycheck pays each bill and what's left over. Weekly, biweekly or monthly pay. Paycheck budget template for Google Sheets and Excel."),
   ("Budget by Paycheck: Assign Every Bill to the Right Payday", "Stop running short before payday: assign each bill to a paycheck and see what's left. Paycheck budget planner spreadsheet."),
   ("Biweekly Budget Planner – Plan Bills Around Your Pay Dates", "Biweekly budget spreadsheet: bills by due date, paycheck summaries and paid checkboxes. Simple paycheck budgeting for beginners."),
   ("Paycheck Budget Template for Beginners – Know What's Left Each Payday", "A simple paycheck budget template that shows what's left from every paycheck after bills. Google Sheets and Excel."),
   ("Bill Planner by Paycheck – Never Miss a Due Date", "Plan every bill by paycheck and mark it paid as you go. Bill planner and paycheck budget spreadsheet, instant download."),
   ("Weekly Paycheck Budget Spreadsheet – Budgeting on a Tight Income", "Budget weekly or biweekly pay on a tight income: see which paycheck can't cover its bills before it happens. Excel and Google Sheets."),
  ]),
 "wedding": dict(
  slug="wedding-budget-planner", name="Wedding Budget Planner", price="6.99", link=G + "odsqq", priority=False,
  images=["v3/pin_wedding_a.jpg", "v3/pin_wedding_b.jpg"],
  blurb="Plan the wedding without the money stress. Split your total budget, compare quotes, and never miss a vendor payment.",
  features=["Budget: 15 categories with a suggested % split, planned vs quoted, paid and still due, cost per guest", "Vendors & payments: deposits and balances with due dates", "Guest list: side, RSVP and meal choice, with automatic counts", "Works in Excel, Google Sheets and Numbers"],
  titles=[
   ("Wedding Budget Spreadsheet – Wedding Planner with Guest List & Vendor Tracker", "Split your wedding budget by category, track vendor deposits and due dates, and manage RSVPs and meals. Google Sheets and Excel."),
   ("Plan Your Wedding Budget Without the Stress", "Wedding budget breakdown by percentage, quotes vs plan and a vendor payment schedule in one wedding planner spreadsheet."),
   ("Wedding Budget Breakdown Template – Percentages for Every Category", "Start from a suggested percentage split for venue, catering, photography and more, then adjust. Wedding budget template."),
   ("Wedding Guest List Spreadsheet with RSVP and Meal Tracker", "Track guests, RSVPs and meal choices with automatic counts, plus your full wedding budget. Wedding planner for Google Sheets."),
   ("Wedding Vendor Payment Tracker – Deposits, Balances and Due Dates", "Never miss a vendor payment: deposits, balances and due dates for every wedding vendor. Wedding budget planner spreadsheet."),
   ("Wedding on a Budget: Cost per Guest Calculator & Budget Planner", "See your cost per guest and where to cut. Affordable wedding budget planner with category split and vendor tracker."),
  ]),
 "freelancer": dict(
  slug="freelancer-income-invoice-tracker", name="Freelancer Income & Invoice Tracker", price="6.99", link=G + "mdfzdj", priority=False, board="biz",
  images=["v3/pin_freelancer_a.jpg", "v3/pin_freelancer_b.jpg"],
  blurb="Know who owes you, what you really earned, and how much to put aside for tax.",
  features=["Invoice log: due dates from your payment terms, OVERDUE alert in red", "Expense log with categories", "Monthly dashboard: income received, expenses, profit, tax set-aside (you pick the %) and what you keep", "Total still owed by clients and average days to get paid"],
  titles=[
   ("Freelancer Invoice Tracker Spreadsheet – Income, Expenses & Tax Set-Aside", "Invoice log with overdue alerts, monthly profit and tax set-aside for self-employed and freelancers. Google Sheets and Excel."),
   ("Freelancers: Know Who Owes You & What to Save for Tax", "Track unpaid invoices, income and expenses and set aside tax every month. Freelancer income tracker spreadsheet."),
   ("Self-Employed Income Tracker – Simple Bookkeeping for Freelancers", "Simple bookkeeping for self-employed people: invoices, expenses, profit and tax set-aside in one spreadsheet."),
   ("Invoice Tracker Template – Overdue Alerts and Payment Status", "See every invoice's status, due date and overdue alert in red. Invoice tracker template for freelancers and small businesses."),
   ("Irregular Income Budget for Freelancers – Profit and Tax Dashboard", "Handle irregular income: monthly dashboard of income received, expenses, profit and what you keep after tax set-aside."),
   ("Side Hustle Income Tracker – Invoices, Expenses and Profit", "Track side hustle income, invoices and expenses and see your real profit each month. Excel and Google Sheets template."),
  ]),
 "debt": dict(
  slug="debt-snowball-avalanche-tracker", name="Debt Snowball & Avalanche Tracker", price="4.99", link=STORE, priority=False,
  images=["debt.jpg", "v2/debt_a.jpg", "v2/debt_b.jpg", "v2/debt_c.jpg"],
  blurb="Compare the debt snowball and debt avalanche methods, rank your debts automatically and see your debt-free date.",
  features=["Snowball vs avalanche side by side", "Debts ranked automatically", "Month-by-month payoff plan", "Debt-free date calculated"],
  titles=[
   ("Debt Snowball Spreadsheet – Get Out of Debt Faster", "Rank your debts and see your debt-free date with a debt snowball spreadsheet. Debt payoff planner for Excel and Google Sheets."),
   ("Debt Payoff Calculator Spreadsheet – See Your Debt-Free Date", "Enter balances and interest rates and see your debt-free date and monthly plan. Credit card payoff tracker template."),
   ("Debt Avalanche vs Snowball Tracker – Which Pays Off Debt Faster?", "Compare debt avalanche and debt snowball side by side and pay less interest. Debt payoff planner spreadsheet."),
   ("Credit Card Payoff Planner – Debt Free Journey Spreadsheet", "Plan your credit card payoff month by month and track progress to debt free. Google Sheets and Excel."),
   ("Debt Tracker Printable & Digital – Pay Off Debt Month by Month", "A debt tracker you can print or use on your phone: balances, payments and payoff order. Debt free planner template."),
  ]),
 "budget": dict(
  slug="50-30-20-monthly-budget-planner", name="50/30/20 Monthly Budget Planner", price="4.99", link=STORE, priority=False,
  images=["budget.jpg", "v2/budget_a.jpg", "v2/budget_b.jpg", "v2/budget_c.jpg"],
  blurb="The easiest budget you'll actually stick to: the 50/30/20 split done for you, with automatic totals and over-budget flags.",
  features=["50/30/20 split done for you", "Auto totals & over-budget flags", "12 monthly tabs + yearly view", "Beginner friendly"],
  titles=[
   ("Monthly Budget Spreadsheet for Beginners – 50/30/20 Budget Template", "A simple monthly budget spreadsheet using the 50/30/20 rule with automatic totals. Budget template for Excel and Google Sheets."),
   ("50/30/20 Budget Planner – Needs, Wants and Savings Made Simple", "Split your income into needs, wants and savings automatically. 50/30/20 budget planner spreadsheet for beginners."),
   ("Simple Budget Template Excel – Monthly Budget Planner", "Planned vs actual spending, over-budget alerts and a yearly summary. Simple monthly budget template."),
   ("How to Budget Your Money: 50/30/20 Budget Spreadsheet", "Learn to budget with the 50/30/20 rule using a ready spreadsheet: needs, wants, savings and monthly tracking."),
   ("Budget Planner Google Sheets – Monthly Budget Tracker", "A monthly budget tracker for Google Sheets and Excel with automatic totals and category flags. Instant download."),
  ]),
 "subscription": dict(
  slug="subscription-bill-tracker", name="Subscription & Bill Tracker", price="4.99", link=STORE, priority=False,
  images=["subscription.jpg", "v2/subscription_a.jpg", "v2/subscription_b.jpg", "v2/subscription_c.jpg"],
  blurb="See what your subscriptions and bills really cost per year — and find what to cancel.",
  features=["Weekly, monthly & annual bills", "Real monthly and yearly cost", "Due-date overview", "Find what to cancel"],
  titles=[
   ("Bill Tracker Spreadsheet – Monthly Bills Organizer", "Every bill and subscription with due dates and real yearly cost. Bill tracker for Google Sheets and Excel."),
   ("Subscription Tracker Template – Find Subscriptions to Cancel", "List your subscriptions and see what they cost per year, then cancel what you don't use. Save money spreadsheet."),
   ("Bill Payment Checklist Spreadsheet – Never Miss a Due Date", "Monthly bill checklist with due dates, billing cycles and yearly totals. Bill organizer template."),
   ("Monthly Bills Tracker – How Much Do Your Subscriptions Really Cost?", "See the true monthly and yearly cost of streaming, gym, phone and more. Subscription audit spreadsheet."),
  ]),
 "habit": dict(
  slug="monthly-habit-tracker", name="Monthly Habit Tracker", price="4.99", link=STORE, priority=False,
  images=["habit.jpg", "v2/habit_a.jpg", "v2/habit_b.jpg", "v2/habit_c.jpg"],
  blurb="Small habits, big results: a 31-day habit grid with automatic completion rates.",
  features=["31-day grid for any month", "Completion rates auto-calculated", "Use on phone or print", "Up to 15 habits"],
  titles=[
   ("Habit Tracker Spreadsheet – Monthly Habit Tracker Google Sheets", "31-day habit grid with automatic completion rates. Habit tracker for Google Sheets and Excel, or print it."),
   ("Printable Habit Tracker – 31 Day Habit Tracker Template", "Track workouts, reading, water and more with a printable 31-day habit tracker. Instant download."),
   ("Digital Habit Tracker with Progress Stats", "A digital daily habit tracker that calculates your completion rate for you. Simple and clean."),
   ("Monthly Habit Tracker for Self-Improvement Goals", "Build better habits month by month with automatic stats. Habit tracker template for Google Sheets."),
  ]),
 "meal": dict(
  slug="weekly-meal-planner-grocery-list", name="Weekly Meal Planner + Grocery List", price="4.99", link=STORE, priority=False,
  images=["meal.jpg", "v2/meal_a.jpg", "v2/meal_b.jpg", "v2/meal_c.jpg"],
  blurb="Plan once, shop once, save every week: a 7-day meal grid with a grocery list.",
  features=["7-day meal grid", "Grocery list with checkboxes", "Weekly food budget", "Reuse every week"],
  titles=[
   ("Weekly Meal Planner Template with Grocery List", "Plan a week of meals in minutes with a weekly meal planner and grocery list. Excel and Google Sheets."),
   ("Meal Plan on a Budget – Printable Meal Planner & Grocery List", "Eat well on a budget: track your weekly food budget and stop wasting food. Meal planning spreadsheet."),
   ("Digital Meal Planner Google Sheets – Family Meal Planning Template", "Breakfast, lunch and dinner grid plus a grocery checklist for busy families. Google Sheets and Excel."),
   ("Grocery Budget Meal Planner – Save Money on Groceries Every Week", "Plan meals around a weekly grocery budget and shop once. Meal planner template, instant download."),
  ]),
 "savings": dict(
  slug="savings-sinking-funds-tracker", name="Savings & Sinking Funds Tracker", price="4.99", link=STORE, priority=False,
  images=["savings.jpg", "v2/savings_a.jpg", "v2/savings_b.jpg", "v2/savings_c.jpg"],
  blurb="Save for everything, stress-free: monthly amounts per goal, countdowns and progress bars.",
  features=["Monthly amount per goal", "Countdown to each target date", "Emergency fund ready", "Progress bars built in"],
  titles=[
   ("Sinking Funds Tracker Spreadsheet – Savings Goals Tracker", "Save for every goal with a sinking funds tracker: monthly amount per goal, progress bars and target dates."),
   ("Emergency Fund Tracker – Savings Tracker Printable & Digital", "Build your emergency fund step by step and watch your progress grow. Savings tracker template."),
   ("Savings Plan Template – How Much to Save Each Month", "Know exactly how much to save per month for vacation, car, gifts and more. Google Sheets and Excel."),
   ("Savings Challenge Tracker Spreadsheet – Reach Your Money Goals", "Track savings goals with countdowns and progress bars. Savings challenge and sinking funds template."),
  ]),
 "networth": dict(
  slug="net-worth-tracker", name="Net Worth Tracker", price="4.99", link=STORE, priority=False,
  images=["networth.jpg", "v2/networth_a.jpg", "v2/networth_b.jpg", "v2/networth_c.jpg"],
  blurb="Watch your wealth grow: assets vs liabilities with monthly history and a growth chart.",
  features=["Assets vs liabilities", "Monthly history auto-linked", "Growth chart included", "Milestones to aim for"],
  titles=[
   ("Net Worth Tracker Spreadsheet – Track Your Net Worth Monthly", "Assets, debts and growth chart month by month. Net worth tracker for Excel and Google Sheets."),
   ("Net Worth Calculator Template – Assets and Liabilities", "List assets and liabilities and see your real net worth with monthly history. Personal finance spreadsheet."),
   ("Wealth Tracker Google Sheets – Financial Freedom Planner", "Stay motivated on your financial freedom journey with monthly net worth, milestones and a growth chart."),
   ("How to Calculate Your Net Worth – Free Your Finances Spreadsheet", "Calculate and track your net worth every month with a simple spreadsheet and growth chart."),
  ]),
 "bookkeeping": dict(
  slug="small-business-bookkeeping", name="Small Business Bookkeeping", price="4.99", link=STORE, priority=False,
  images=["bookkeeping.jpg", "v2/bookkeeping_a.jpg", "v2/bookkeeping_b.jpg", "v2/bookkeeping_c.jpg"],
  blurb="Bookkeeping without the headache: income, expenses and profit in one sheet.",
  features=["Income & expense log", "Category summary, linked", "Monthly profit & loss", "No accounting app needed"],
  titles=[
   ("Small Business Bookkeeping Template – Income & Expense Spreadsheet", "Log income and expenses and get a monthly profit and loss automatically. Excel and Google Sheets."),
   ("Expense Tracker for Small Business – Profit & Loss Template", "Track business income and expenses with a linked profit and loss summary. Great for Etsy sellers and side hustles."),
   ("Bookkeeping Spreadsheet for Etsy Sellers & Side Hustles", "Easy bookkeeping for Etsy sellers and freelancers: categories, monthly summary and profit."),
   ("Simple Bookkeeping Template – No Accounting App Needed", "Simple income and expense tracker with monthly profit for small business owners."),
  ]),
 "metaads": dict(
  slug="meta-ads-campaign-tracker", name="Meta Ads Campaign Tracker", price="4.99", link=STORE, priority=False,
  images=["metaads.jpg", "v2/metaads_a.jpg", "v2/metaads_b.jpg", "v2/metaads_c.jpg"],
  blurb="Know which ads make money: ROAS, CPA and CTR in one clean dashboard.",
  features=["ROAS, CPA & CTR auto-calculated", "Per-campaign spend log", "Facebook & Instagram ads", "Weekly performance view"],
  titles=[
   ("Facebook Ads Tracker Spreadsheet – Track ROAS & CPA", "Know which Facebook ads make money: ROAS, CPA and CTR per campaign. Google Sheets and Excel."),
   ("Meta Ads Reporting Template for Small Business", "Log ad spend and results and get ROAS and CPA automatically. Meta ads reporting spreadsheet."),
   ("Ad Spend Tracker for Ecommerce – Instagram & Facebook Ads", "Track ad spend and results across Instagram and Facebook ads with weekly performance view."),
   ("ROAS Calculator Spreadsheet – Facebook Ads Campaign Tracker", "Calculate ROAS and CPA for every campaign and see what to scale. Ads tracker template."),
  ]),
}

# image file -> product key (so schedule.json entries can be mapped back to a product)
IMAGE_TO_PRODUCT = {img.split("/")[-1]: k for k, p in PRODUCTS.items() for img in p["images"]}
