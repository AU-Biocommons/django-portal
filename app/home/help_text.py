"""Help text for model fields."""

MARKDOWN_HELP_TEXT = (
    """Enter valid GitHub markdown -
    <a href="https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax" target="_blank">see markdown guide</a>.
    We're using <b>"code-friendly" mode</b>, so __ and _ will be rendered
    literally! Use * and ** for italics/bold instead. HTML is also fine.
    """
)


class Notice:
    """Help text for Notice model fields."""

    NOTICE_CLASS = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            A style class to set a color scheme for the notice - uses
            <a
                href='https://getbootstrap.com/docs/5.0/components/alerts/'
                target='_blank'
            >standard bootstrap styling</a>
            (<em>info</em>: blue, <em>warning</em>: orange).
        </li>
    </ul>
    """

    TITLE = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            This will be displayed on the landing page (200 char max) as plain
            text or inline HTML (e.g.
            <code>&lt;em&gt;</code>,
            <code>&lt;b&gt;</code>
            tags).
        </li>
        <li style='list-style: disc;'>
            No <code>&lt;a&gt;</code> tags please, as this creates a confusing
            user experience (link within link).
        </li>
        <li style='list-style: disc;'>
            This will be shown as a single line of text above the navbar,
            <b>which will be cut off if too long</b>,
            especially on small screens! Please check the length is reasonable
            before publishing the notice.
        </li>
    </ul>
    """

    BODY = f"""
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            {MARKDOWN_HELP_TEXT}
        </li>
        <li style='list-style: disc;'>
            <b>This text will be displayed on a dedicated webpage</b>
            that is linked to from the landing page notice.
            If this field is left blank, there will be no link.
        </li>
    </ul>
    """

    MATERIAL_ICON = """
    Optional. A valid Material Design icon ID to be displayed with the title
    (e.g. <em>check_box</em>).
    <a href="https://fonts.google.com/icons" target="_blank">
    Browse 2500+ icons here
    </a>.
    """
