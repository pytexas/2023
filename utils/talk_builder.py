import collections
import datetime
import json
import pathlib
import zoneinfo

PROJECT_ROOT = pathlib.Path(__file__).parents[1]
SCHEDULE_DIR = PROJECT_ROOT / "content" / "schedule"
TALK_FILE = SCHEDULE_DIR / "talks.md"
SCHEDULE_FILE = SCHEDULE_DIR / "schedule.md"

TALKS_HEADER = """Title: Talks
slug: schedule/talks
date: 2023-02-14

# Accepted Talks
---

These are the talks accepted to PyTexas,
listed in no particular order.
A full schedule will be released closer to the conference.

---"""


TALK_TEMPLATE = """<h2>
    Talk:
    <a id="{talk_id}">{title}</a>
</h2>
<p>{abstract}</p>
{speaker_bios}
"""

SPEAKER_BIO_TEMPLATE = """<div class="media">
    <div class="col-2">
        <img class="align-self-start mr-3 img-thumbnail" src="{picture}">
    </div>
    <div class="media-body">
        <h5 class="mt-0">
            Speaker: {name}
        </h5>
        <small>
            {bio}
        </small>
    </div>
</div>"""

SCHEDULE_PAGE_TEMPLATE = """Title: Full Schedule
slug: schedule
date: 2023-02-16
# Talk Schedule

_This schedule may change at any time between now and the start of the conference._

<table class="table">
  <thead class="thead-dark">
    <th width="20%" scope="col">Time</th>
    <th style="text-align:center;" scope="col">Saturday</th>
    <th style="text-align:center;" scope="col">Sunday</th>
  </thead>
  <tbody>
  {rows}
  </tbody>
</table>
"""

SCHEDULE_ROW_TEMPLATE = """<tr>
    <th scope="row">{schedule_time}</th>
    {first_entry}
    {second_entry}
</tr>"""

SCHEDULE_ENTRY_TEMPLATE = """<td>
    <p style="text-align:center;">
        <a href="{href}">{title}</a>
    </p>
    <p style="text-align:center;font-size:16px;">{speaker_names}</p>
</td>"""

SIMPLE_CELL = """<td style="text-align:center">{}</td>"""


STATIC_EVENTS = {
    datetime.time(9, 0): [
        SIMPLE_CELL.format("Day 1 Opening Remarks"),
        SIMPLE_CELL.format("Day 2 Opening Remarks"),
    ],
    datetime.time(9, 15): [
        SCHEDULE_ENTRY_TEMPLATE.format(
            href="schedule/keynotes/", title="Keynote", speaker_names="Brandon Rhodes"
        ),
        SCHEDULE_ENTRY_TEMPLATE.format(
            href="schedule/keynotes/", title="Keynote", speaker_names="Andy Knight"
        ),
    ],
    datetime.time(10, 0): [SIMPLE_CELL.format("15 Minute Break")] * 2,
    datetime.time(12, 15): [SIMPLE_CELL.format("Lunch")] * 2,
    datetime.time(15, 15): [SIMPLE_CELL.format("15 Minute Break")] * 2,
    datetime.time(17, 0): [SIMPLE_CELL.format("Lighnting Talks")] * 2,
}


def _get_file(name: str):
    source = PROJECT_ROOT / "data" / f"{name}.json"
    return json.loads(source.read_text())


def get_talks():
    return _get_file("sessions")


def get_speakers():
    return _get_file("speakers")


def _format_speaker(data):
    picture = data["Picture"] or "/theme/img/2023-logo.png"
    bio = data["Biography"] or ""
    return SPEAKER_BIO_TEMPLATE.format(name=data["Name"], picture=picture, bio=bio)


def format_talks(talk_data: dict, speakers):
    talk_id = talk_data["ID"]
    title = talk_data["Proposal title"]

    speaker_bios = []
    for speaker_data in speakers:
        speaker_bios.append(_format_speaker(speaker_data))

    speaker_str = "\n".join(speaker_bios)

    talk_entry = TALK_TEMPLATE.format(
        talk_id=talk_id,
        title=title,
        abstract=talk_data["Abstract"],
        speaker_bios=speaker_str,
    )
    return talk_entry


def build_talk_entries(talks, speakers):
    talk_entries = []
    for talk in talks:
        talk_speakers = [s for s in speakers if s["ID"] in talk["Speaker IDs"]]
        talk_entry = format_talks(talk, talk_speakers)
        talk_entries.append(talk_entry)
    return talk_entries


def _format_schedule_entry(talk):
    return SCHEDULE_ENTRY_TEMPLATE.format(
        title=talk["Proposal title"],
        href=f"schedule/talks/#{talk['ID']}",
        speaker_names=", ".join(talk["Speaker names"]),
    )


def build_schedule_rows(talks, speakers):
    scheduled_talks = sorted(
        [t for t in talks if t["Start"]],
        key=lambda t: datetime.datetime.fromisoformat(t["Start"]),
    )
    talks_by_date = collections.defaultdict(dict)
    local_tz = zoneinfo.ZoneInfo("US/Central")
    for talk in scheduled_talks:
        start_dt = datetime.datetime.fromisoformat(talk["Start"]).astimezone(local_tz)
        talks_by_date[start_dt.time()][start_dt.date()] = _format_schedule_entry(talk)

    talks_by_time = {**STATIC_EVENTS}
    for time_dt, talk_dict in talks_by_date.items():
        time_talks = [talk_dict[k] for k in sorted(talk_dict)]
        talks_by_time[time_dt] = time_talks

    schedule_rows = []
    for timeslot in sorted(talks_by_time):
        time_str = timeslot.strftime("%I:%M %p")
        timeslot_talks = talks_by_time[timeslot]
        if len(talks_by_time[timeslot]) != 2:
            # There is one special-case where a Saturday talk is not yet assigned
            timeslot_talks = [SIMPLE_CELL.format("TBA"), timeslot_talks[0]]
        first_entry, second_entry = timeslot_talks
        schedule_rows.append(
            SCHEDULE_ROW_TEMPLATE.format(
                schedule_time=time_str,
                first_entry=first_entry,
                second_entry=second_entry,
            )
        )
    return schedule_rows


def write_talks(talk_entries):
    talks = "\n<br><br>\n".join(talk_entries)
    talk_content = f"{TALKS_HEADER}\n\n{talks}"
    TALK_FILE.write_text(talk_content)


def write_schedule(schedule_entries):
    rows = "\n".join(schedule_entries)
    schedule_content = SCHEDULE_PAGE_TEMPLATE.format(rows=rows)
    SCHEDULE_FILE.write_text(schedule_content)


def write_pages():
    talks = get_talks()
    speakers = get_speakers()
    write_talks(build_talk_entries(talks, speakers))
    write_schedule(build_schedule_rows(talks, speakers))


if __name__ == "__main__":
    write_pages()
