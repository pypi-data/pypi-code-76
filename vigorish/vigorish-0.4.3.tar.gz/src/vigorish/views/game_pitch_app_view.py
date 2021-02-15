from sqlalchemy import func, join, select
from sqlalchemy_utils import create_view

import vigorish.database as db


class Game_PitchApp_View(db.Base):
    __table__ = create_view(
        name="game_pitch_app_status",
        selectable=select(
            [
                db.GameScrapeStatus.id.label("id"),
                db.GameScrapeStatus.bbref_game_id.label("bbref_game_id"),
                func.count(db.PitchAppScrapeStatus.id).label("total_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.scraped_pitchfx).label("total_pitchfx_scraped"),
                func.sum(db.PitchAppScrapeStatus.no_pitchfx_data).label("total_no_pitchfx_data"),
                func.sum(db.PitchAppScrapeStatus.combined_pitchfx_bbref_data).label(
                    "total_combined_pitchfx_bbref_data"
                ),
                func.sum(db.PitchAppScrapeStatus.batters_faced_bbref).label("total_batters_faced_bbref"),
                func.sum(db.PitchAppScrapeStatus.batters_faced_pitchfx).label("total_batters_faced_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.duplicate_guid_removed_count).label(
                    "total_duplicate_pitchfx_removed_count"
                ),
                func.sum(db.PitchAppScrapeStatus.pitch_count_pitch_log).label("total_pitch_count_pitch_log"),
                func.sum(db.PitchAppScrapeStatus.pitch_count_bbref).label("total_pitch_count_bbref"),
                func.sum(db.PitchAppScrapeStatus.pitch_count_pitchfx).label("total_pitch_count_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.pitch_count_pitchfx_audited).label(
                    "total_pitch_count_pitchfx_audited"
                ),
                func.sum(db.PitchAppScrapeStatus.patched_pitchfx_count).label("total_patched_pitchfx_count"),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_pitchfx_complete).label(
                    "total_at_bats_pitchfx_complete"
                ),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_patched_pitchfx).label("total_at_bats_patched_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.missing_pitchfx_count).label("total_missing_pitchfx_count"),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_missing_pitchfx).label("total_at_bats_missing_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.extra_pitchfx_count).label("total_extra_pitchfx_count"),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_extra_pitchfx).label("total_at_bats_extra_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.extra_pitchfx_removed_count).label(
                    "total_extra_pitchfx_removed_count"
                ),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_extra_pitchfx_removed).label(
                    "total_at_bats_extra_pitchfx_removed"
                ),
                func.sum(db.PitchAppScrapeStatus.pitchfx_error).label("total_pitchfx_error"),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_pitchfx_error).label("total_at_bats_pitchfx_error"),
                func.sum(db.PitchAppScrapeStatus.invalid_pitchfx).label("total_invalid_pitchfx"),
                func.sum(db.PitchAppScrapeStatus.invalid_pitchfx_count).label("total_invalid_pitchfx_count"),
                func.sum(db.PitchAppScrapeStatus.total_at_bats_invalid_pitchfx).label("total_at_bats_invalid_pitchfx"),
            ]
        )
        .select_from(
            join(
                db.GameScrapeStatus,
                db.PitchAppScrapeStatus,
                db.GameScrapeStatus.id == db.PitchAppScrapeStatus.scrape_status_game_id,
            )
        )
        .group_by(db.GameScrapeStatus.id),
        metadata=db.Base.metadata,
        cascade_on_drop=False,
    )
