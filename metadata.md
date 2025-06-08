{
  "file_name": "full_dataset.csv",
  "description": "Weekly sales, inventory, and forecast data for various product models, including uplifted sales, coverage, trend, and event features. Used for demand forecasting, inventory management, and sales analysis.",
  "columns": [
    {
      "name": "covfsmcmodelweekkey",
      "type": "string",
      "description": "Unique identifier for each record, a concatenation of model, week, and year."
    },
    {
      "name": "model",
      "type": "string",
      "description": "Product model code."
    },
    {
      "name": "week",
      "type": "integer",
      "description": "ISO week number of the year."
    },
    {
      "name": "Week_start_date",
      "type": "datetime",
      "description": "Start date of the week (ISO format)."
    },
    {
      "name": "Week_end_date",
      "type": "datetime",
      "description": "End date of the week (ISO format)."
    },
    {
      "name": "End_month",
      "type": "integer",
      "description": "Month number in which the week ends."
    },
    {
      "name": "WeekNum",
      "type": "integer",
      "description": "Sequential week number within the year."
    },
    {
      "name": "Year",
      "type": "integer",
      "description": "Calendar year."
    },
    {
      "name": "13w_sellout",
      "type": "float",
      "description": "Total sell-out units over the past 13 weeks."
    },
    {
      "name": "13w_coverage_calc",
      "type": "float",
      "description": "Calculated coverage (weeks) based on 13-week sell-out."
    },
    {
      "name": "raw_sell_out",
      "type": "float",
      "description": "Raw sell-out units for the week."
    },
    {
      "name": "rawsoh",
      "type": "float",
      "description": "Raw stock on hand at the end of the week."
    },
    {
      "name": "13w_opening_soh",
      "type": "float",
      "description": "Stock on hand at the start of the 13-week period."
    },
    {
      "name": "13w_closing_soh",
      "type": "float",
      "description": "Stock on hand at the end of the 13-week period."
    },
    {
      "name": "13w_sellinincl",
      "type": "float",
      "description": "Total sell-in units included over the past 13 weeks."
    },
    {
      "name": "average_10wk_coverage",
      "type": "float",
      "description": "Average coverage (weeks) over the past 10 weeks."
    },
    {
      "name": "rawsellinttl",
      "type": "float",
      "description": "Total raw sell-in units for the week."
    },
    {
      "name": "uplifted_sell_out",
      "type": "float",
      "description": "Sell-out units after applying uplift (e.g., promotional adjustment)."
    },
    {
      "name": "13w_uplifted_sell_out_avg",
      "type": "float",
      "description": "Average uplifted sell-out over the past 13 weeks."
    },
    {
      "name": "25w_uplifted_sell_out_avg",
      "type": "float",
      "description": "Average uplifted sell-out over the past 25 weeks."
    },
    {
      "name": "25w_13w_diff",
      "type": "float",
      "description": "Difference between 25-week and 13-week average uplifted sell-out."
    },
    {
      "name": "53w_uplifted_sell_out_avg",
      "type": "float",
      "description": "Average uplifted sell-out over the past 53 weeks."
    },
    {
      "name": "53w_25w_diff",
      "type": "float",
      "description": "Difference between 53-week and 25-week average uplifted sell-out."
    },
    {
      "name": "5w_uplifted_sell_out_avg",
      "type": "float",
      "description": "Average uplifted sell-out over the past 5 weeks."
    },
    {
      "name": "13w_5w_diff",
      "type": "float",
      "description": "Difference between 13-week and 5-week average uplifted sell-out."
    },
    {
      "name": "rolling_uplifted_sell_out_sum",
      "type": "float",
      "description": "Rolling sum of uplifted sell-out units."
    },
    {
      "name": "STL_trend",
      "type": "float",
      "description": "Trend component from STL (Seasonal-Trend decomposition) analysis."
    },
    {
      "name": "STL_seasonal",
      "type": "float",
      "description": "Seasonal component from STL decomposition."
    },
    {
      "name": "STL_resid",
      "type": "float",
      "description": "Residual component from STL decomposition."
    },
    {
      "name": "body_sellout",
      "type": "float",
      "description": "Sell-out units for the main (body) product."
    },
    {
      "name": "yearweek",
      "type": "string",
      "description": "Combined year and week identifier (ISO format)."
    },
    {
      "name": "sales",
      "type": "float",
      "description": "Sales units for the week."
    },
    {
      "name": "sale_category",
      "type": "string",
      "description": "Category of sale event (e.g., Major, Minor, No)."
    },
    {
      "name": "weeks_since_major",
      "type": "integer",
      "description": "Number of weeks since the last major event."
    },
    {
      "name": "basic_material",
      "type": "string",
      "description": "Basic material or product code."
    },
    {
      "name": "product_group",
      "type": "string",
      "description": "Product group/category."
    },
    {
      "name": "sub_group",
      "type": "string",
      "description": "Product sub-group/category."
    },
    {
      "name": "market_level",
      "type": "string",
      "description": "Market level or segmentation."
    },
    {
      "name": "product_hierarchy",
      "type": "string",
      "description": "Full product hierarchy code."
    },
    {
      "name": "release_year_MM",
      "type": "integer",
      "description": "Release year and month (YYYY or YYYYMM)."
    },
    {
      "name": "OSD",
      "type": "datetime",
      "description": "Original Start Date or On-Shelf Date for the product."
    },
    {
      "name": "days_since_osd",
      "type": "integer",
      "description": "Days since the product's OSD."
    },
    {
      "name": "uplifted_sell_out_lag1",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 1 week."
    },
    {
      "name": "uplifted_sell_out_lag2",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 2 weeks."
    },
    {
      "name": "uplifted_sell_out_lag3",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 3 weeks."
    },
    {
      "name": "uplifted_sell_out_lag4",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 4 weeks."
    },
    {
      "name": "uplifted_sell_out_lag5",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 5 weeks."
    },
    {
      "name": "uplifted_sell_out_lag6",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 6 weeks."
    },
    {
      "name": "uplifted_sell_out_lag7",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 7 weeks."
    },
    {
      "name": "uplifted_sell_out_lag8",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 8 weeks."
    },
    {
      "name": "uplifted_sell_out_lag9",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 9 weeks."
    },
    {
      "name": "uplifted_sell_out_lag10",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 10 weeks."
    },
    {
      "name": "uplifted_sell_out_lag11",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 11 weeks."
    },
    {
      "name": "uplifted_sell_out_lag12",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 12 weeks."
    },
    {
      "name": "uplifted_sell_out_lag51",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 51 weeks."
    },
    {
      "name": "uplifted_sell_out_lag52",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 52 weeks."
    },
    {
      "name": "uplifted_sell_out_lag53",
      "type": "float",
      "description": "Uplifted sell-out value lagged by 53 weeks."
    },
    {
      "name": "uplifted_sell_out_lag_diff1",
      "type": "float",
      "description": "Difference between current and lag1 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff2",
      "type": "float",
      "description": "Difference between current and lag2 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff3",
      "type": "float",
      "description": "Difference between current and lag3 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff4",
      "type": "float",
      "description": "Difference between current and lag4 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff5",
      "type": "float",
      "description": "Difference between current and lag5 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff6",
      "type": "float",
      "description": "Difference between current and lag6 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff7",
      "type": "float",
      "description": "Difference between current and lag7 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff8",
      "type": "float",
      "description": "Difference between current and lag8 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff9",
      "type": "float",
      "description": "Difference between current and lag9 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff10",
      "type": "float",
      "description": "Difference between current and lag10 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff11",
      "type": "float",
      "description": "Difference between current and lag11 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff12",
      "type": "float",
      "description": "Difference between current and lag12 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff51",
      "type": "float",
      "description": "Difference between current and lag51 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff52",
      "type": "float",
      "description": "Difference between current and lag52 uplifted sell-out."
    },
    {
      "name": "uplifted_sell_out_lag_diff53",
      "type": "float",
      "description": "Difference between current and lag53 uplifted sell-out."
    }
  ]
}
