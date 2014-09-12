"""
Artists classes for rendering data to screen.

Unlike styluses, artists may contain the data that they render. Think of an
artist as a bridge between data and styluses. For example, line artists, marker
artists, and bar artists, may all be the same data associated with different
artists. Note that artists may not map directly to styluses: A scatter artist
uses a marker stylus, but a line artist might have *both* line and marker
styluses.

"""
