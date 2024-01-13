from datetime import datetime
from typing import Dict, List

from aiogoogle import Aiogoogle

from constants import G_FORMAT, G_VERSION_DRIVE, G_VERSION_SHEETS
from core.config import settings
from service_constants import SPREADSHEETS_BODY


async def spreadsheets_create(wrapper_services: Aiogoogle,
                              spreadsheets_body: dict = SPREADSHEETS_BODY) -> str:
    """Создаем пустую таблицу"""
    now_date_time = datetime.now().strftime(G_FORMAT)
    spreadsheets_body_copy = SPREADSHEETS_BODY.copy()
    spreadsheets_body_copy['properties']['title'] = f'QRKot_Отчет на {now_date_time}'
    service = await wrapper_services.discover('sheets', G_VERSION_SHEETS)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Доступ к таблице для личного аккаунта"""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', G_VERSION_DRIVE)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[Dict[str, str]],
    wrapper_services: Aiogoogle
) -> None:
    """Заполняем таблицу отчетом о закрытых проектах"""
    service = await wrapper_services.discover('sheets', G_VERSION_SHEETS)
    table_values = [
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
        *[list(map(str, project.values())) for project in projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    all_lines = len(table_values)
    if all_lines < 100:
        await wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range=f'R1C1:R{all_lines}C{all_lines}',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
    else:
        raise Exception('Слишком много строк')
