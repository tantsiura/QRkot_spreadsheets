from constants import G_COLUMN_COUNT, G_LOCALE, G_ROW_COUNT, G_SHEET_ID, G_TITLE_CLOSE_SPEED


SPREADSHEETS_BODY = dict(
    properties=dict(
        title='',
        locale=G_LOCALE
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=G_SHEET_ID,
        title=G_TITLE_CLOSE_SPEED,
        gridProperties=dict(
            rowCount=G_ROW_COUNT,
            columnCount=G_COLUMN_COUNT
        )
    ))]
)
