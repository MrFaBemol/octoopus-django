from what.models import Instrument


def get_instrument_parent_category(instrument_id=0):
    instrument = Instrument.objects.get(id=instrument_id)
    # return get_instrument_full_name(instrument.parent_id.id) + '/' + instrument.name if instrument.parent_id else instrument.name
    return get_instrument_parent_category(instrument.parent_id.id) + instrument.parent_id.name + "/" if instrument.parent_id else ""

