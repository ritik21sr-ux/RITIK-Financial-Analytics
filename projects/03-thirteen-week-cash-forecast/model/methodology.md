# Forecast methodology

## Weekly cash bridge

`Closing cash = Opening cash + expected customer receipts + other inflows - supplier payments - payroll - fixed operating costs - scenario-adjusted discretionary costs - capital spending`

The first week uses the editable opening cash assumption. Each later week opens at the prior week's closing cash. Customer receipts use invoice amount × collection probability × scenario factor, capped at 100% collection. The Base scenario uses a factor of 1.00; Downside uses 0.75; Upside uses 1.05. Discretionary operating cost uses 1.00, 1.08, and 0.97 respectively.

## Inputs and outputs

The AR, AP, and weekly operating schedules are separate input sheets. The weekly forecast sums each schedule by week, so users can inspect the source lines behind the cash bridge. The dashboard shows closing cash against an editable minimum cash floor.

## Limitations

This simplified model has no debt facility, tax, interest, foreign exchange, restricted cash, payment batching, or intra-week timing. Expected receipts are not guaranteed collections. Change the assumptions only after validating source schedules and opening bank cash.
