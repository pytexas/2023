import json
import pathlib

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

SCHEDULE_ENTRY_TEMPLATE = """<tr>
    <th scope="row">{schedule_time}</th>
    <td>
        <p style="text-align:center;">
            <a href="talks/#{talk_id}">{title}</a>
        </p>
        <p style="text-align:center;font-size:16px;">{speaker_names}</p>
    </td>
</tr>"""


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


def build_schedule_entries(talks, speakers):
    pass


def write_talks(talk_entries):
    talks = "\n\n".join(talk_entries)
    talk_content = f"{TALKS_HEADER}\n\n{talks}"
    TALK_FILE.write_text(talk_content)


def write_schedule(schedule_entries):
    pass


def write_pages():
    talks = get_talks()
    speakers = get_speakers()
    write_talks(build_talk_entries(talks, speakers))
    write_schedule(build_schedule_entries(talks, speakers))


if __name__ == "__main__":
    write_pages()
