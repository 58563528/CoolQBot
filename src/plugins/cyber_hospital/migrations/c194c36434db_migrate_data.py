"""migrate data

修订 ID: c194c36434db
父修订: 3c6992cc96cf
创建时间: 2023-10-29 18:34:04.768866

"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
from nonebot import logger
from sqlalchemy import Connection, inspect, select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

revision: str = "c194c36434db"
down_revision: str | Sequence[str] | None = "3c6992cc96cf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _migrate_old_data(ds_conn: Connection):
    insp = inspect(ds_conn)
    if (
        "cyber_hospital_patient" not in insp.get_table_names()
        or "cyber_hospital_alembic_version" not in insp.get_table_names()
    ):
        logger.info("cyber_hospital: 未发现来自 datastore 的数据")
        return

    DsBase = automap_base()
    DsBase.prepare(autoload_with=ds_conn)
    ds_session = Session(ds_conn)

    AlembicVersion = DsBase.classes.cyber_hospital_alembic_version
    version_num = ds_session.scalars(select(AlembicVersion.version_num)).one_or_none()
    if not version_num:
        return
    if version_num != "8c5eecbd81fd":
        logger.warning(
            "cyber_hospital: 发现旧版本的数据，请先安装 0.16.1 版本，"
            "并运行 nb datastore upgrade 完成数据迁移之后再安装新版本"
        )
        raise RuntimeError("cyber_hospital: 请先安装 0.16.1 版本完成迁移之后再升级")

    DsPatient = DsBase.classes.cyber_hospital_patient
    DsRecord = DsBase.classes.cyber_hospital_record

    Base = automap_base()
    Base.prepare(autoload_with=op.get_bind())
    session = Session(op.get_bind())

    Patient = Base.classes.cyber_hospital_patient
    Record = Base.classes.cyber_hospital_record

    # 写入数据
    logger.info("cyber_hospital: 发现来自 datastore 的数据，正在迁移...")
    for ds_patient in ds_session.query(DsPatient).all():
        patient = Patient(
            id=ds_patient.id,
            user_id=ds_patient.user_id,
            group_id=ds_patient.group_id,
            admitted_at=ds_patient.admitted_at,
            discharged_at=ds_patient.discharged_at,
        )
        session.add(patient)
    for ds_record in ds_session.query(DsRecord).all():
        record = Record(
            id=ds_record.id,
            patient_id=ds_record.patient_id,
            time=ds_record.time,
            content=ds_record.content,
        )
        session.add(record)

    session.commit()
    logger.info("cyber_hospital: 迁移完成")


async def data_migrate(conn: AsyncConnection):
    from nonebot_plugin_datastore.db import get_engine

    async with get_engine().connect() as ds_conn:
        await ds_conn.run_sync(_migrate_old_data)


def upgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    op.run_async(data_migrate)
    # ### end Alembic commands ###


def downgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
