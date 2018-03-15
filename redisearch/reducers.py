from .aggregation import Reducer, SortDirection


class FieldOnlyReducer(Reducer):
    def __init__(self, field):
        super(FieldOnlyReducer, self).__init__(field)
        self._field = field


class count(Reducer):
    """
    Counts the number of results in the group
    """
    NAME = 'COUNT'

    def __init__(self):
        super(count, self).__init__()


class sum(FieldOnlyReducer):
    """
    Calculates the sum of all the values in the given fields within the group
    """
    NAME = 'SUM'

    def __init__(self, field):
        super(sum, self).__init__(field)


class min(FieldOnlyReducer):
    """
    Calculates the smallest value in the given field within the group
    """
    NAME = 'MIN'

    def __init__(self, field):
        super(min, self).__init__(field)


class max(FieldOnlyReducer):
    """
    Calculates the largest value in the given field within the group
    """
    NAME = 'MAX'

    def __init__(self, field):
        super(max, self).__init__(field)


class avg(FieldOnlyReducer):
    """
    Calculates the mean value in the given field within the group
    """
    NAME = 'AVG'

    def __init__(self, field):
        super(avg, self).__init__(field)


class count_distinct(FieldOnlyReducer):
    """
    Calculate the number of distinct values contained in all the results in
    the group for the given field
    """
    NAME = 'COUNT_DISTINCT'

    def __init__(self, field):
        super(count_distinct, self).__init__(field)


class count_distinctish(FieldOnlyReducer):
    """
    Calculate the number of distinct values contained in all the results in the
    group for the given field. This uses a faster algorithm than
    `count_distinct` but is less accurate
    """
    name = 'COUNT_DISTINCTISH'


class quantile(Reducer):
    """
    Return the value for the nth percentile within the range of values for the
    field within the group.
    """
    NAME = 'QUANTILE'

    def __init__(self, field, pct):
        super(quantile, self).__init__(field, pct)
        self._field = field


class stddev(FieldOnlyReducer):
    """
    Return the standard deviation for the values within the group
    """
    name = 'STDDEV'

    def __init__(self, field):
        super(stddev, self).__init__(field)


class first_value(Reducer):
    """
    Selects the first value within the group according to sorting parameters
    """
    NAME = 'FIRST_VALUE'

    def __init__(self, field, *byfields):
        """
        Selects the first value of the given field within the group.

        ### Parameter

        - **field**: Source field used for the value
        - **byfields**: How to sort the results. This can be either the
            *class* of `aggregation.Asc` or `aggregation.Desc` in which
            case the field `field` is also used as the sort input.

            `byfields` can also be one or more *instances* of `Asc` or `Desc`
            indicating the sort order for these fields
        """
        fieldstrs = []
        if len(byfields) == 1 and isinstance(byfields[0], type) and \
                issubclass(byfields[0], SortDirection):
            byfields = [byfields[0](field)]

        for f in byfields:
            fieldstrs += [f.field, f.DIRSTRING]

        args = [field]
        if fieldstrs:
            args += ['BY'] + fieldstrs
        super(first_value, self).__init__(*args)
        self._field = field
