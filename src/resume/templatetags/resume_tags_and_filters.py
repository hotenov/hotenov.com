"""Custom filters and tags."""
import re

from django import template


register = template.Library()


@register.filter(name="cut_regex", is_safe=True)
def cut_regex(value, search):
    """Cut string by regex pattern."""
    return re.sub(search, "", value)


@register.filter(name="split", is_safe=True)
def split_filter(value, separator=" "):
    """Split string by specified separator."""
    return value.split(separator)


@register.filter(name="splitlines", is_safe=True)
def splitlines_filter(value, keepends=False):
    """Split string by specified separator."""
    if not keepends:
        return value.splitlines()
    else:
        return value.splitlines(keepends=True)


@register.filter(name="parse_contacts", is_safe=True)
def parse_contacts(contact_lines):
    """Parse list of lines with contact information."""
    contacts_list = []
    for line in contact_lines:
        if "||" in line:
            contact = line.strip().split("||")
            contacts_list.append(contact)
        else:
            contacts_list.append([line.strip(), "-", ""])
    return contacts_list


@register.filter(name="parse_instruments", is_safe=True)
def parse_instruments(instrument_lines):
    """Parse list of lines with instruments (relevant skills)."""
    instruments_dict = {}
    for line in instrument_lines:
        if ":" in line:
            k, v = line.strip().split(":", 1)
            instruments_dict[k.strip()] = v.strip()
        else:
            instruments_dict[line.strip()] = ""
    return instruments_dict


@register.filter(name="parse_skills", is_safe=True)
def parse_skills(skill_lines):
    """Parse list of lines with skills."""
    skills_dict = {}
    for line in skill_lines:
        if "=" in line:
            k, v = line.strip().split("=")
            skills_dict[k.strip()] = int(v.strip())
        else:
            skills_dict[line.strip()] = 33
    return skills_dict


@register.filter(name="filesize_for_humans", is_safe=True)
def filesize_filter(filesize, suffix="B"):
    """Represent filesize like a 'human-readable' with full names."""
    # You can add more values if you use large files
    full = {"-": "", "K": "Kilo", "M": "Mega"}
    num = filesize
    for unit in ("-", "K", "M"):
        if num < 1024.0:
            return (
                f"{num:3.1f}",
                f"{unit}{suffix}",
                f"{full[unit]}bytes",
            )
        num /= 1024.0
