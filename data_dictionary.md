\# Mutual Fund Analytics Data Dictionary





\## fact\_nav



|Column|Type|Description|

|-|-|-|

|amfi\_code|INTEGER|Mutual fund identifier|

|date|DATE|NAV date|

|nav|REAL|Net Asset Value|





\## fact\_transactions



|Column|Type|Description|

|-|-|-|

|investor\_id|INTEGER|Investor ID|

|transaction\_date|DATE|Transaction date|

|amfi\_code|INTEGER|Fund identifier|

|transaction\_type|TEXT|SIP/LUMPSUM/REDEMPTION|

|amount\_inr|REAL|Transaction amount|

|state|TEXT|Investor state|

|city|TEXT|Investor city|

|kyc\_status|TEXT|KYC verification status|





\## fact\_performance



|Column|Type|Description|

|-|-|-|

|amfi\_code|INTEGER|Fund identifier|

|scheme\_name|TEXT|Scheme name|

|fund\_house|TEXT|AMC name|

|return\_1yr\_pct|REAL|1 year return|

|return\_3yr\_pct|REAL|3 year return|

|return\_5yr\_pct|REAL|5 year return|

|expense\_ratio\_pct|REAL|Expense ratio|

|aum\_crore|REAL|Assets under management|





Source:

data/raw CSV files

