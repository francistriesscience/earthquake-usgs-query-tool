def build_query_params(args):
    params = {}

    # Format
    params['format'] = args.format

    # Time parameters
    if args.starttime:
        params['starttime'] = args.starttime
    if args.endtime:
        params['endtime'] = args.endtime
    if args.updatedafter:
        params['updatedafter'] = args.updatedafter

    # Location parameters - Rectangle
    if args.minlatitude is not None:
        params['minlatitude'] = args.minlatitude
    if args.maxlatitude is not None:
        params['maxlatitude'] = args.maxlatitude
    if args.minlongitude is not None:
        params['minlongitude'] = args.minlongitude
    if args.maxlongitude is not None:
        params['maxlongitude'] = args.maxlongitude

    # Location parameters - Circle
    if args.latitude is not None and args.longitude is not None and args.maxradius is not None:
        params['latitude'] = args.latitude
        params['longitude'] = args.longitude
        params['maxradius'] = args.maxradius
    elif args.latitude is not None and args.longitude is not None and args.maxradiuskm is not None:
        params['latitude'] = args.latitude
        params['longitude'] = args.longitude
        params['maxradiuskm'] = args.maxradiuskm

    # Other parameters
    if args.catalog:
        params['catalog'] = args.catalog
    if args.contributor:
        params['contributor'] = args.contributor
    if args.eventid:
        params['eventid'] = args.eventid
    if args.includeallmagnitudes:
        params['includeallmagnitudes'] = 'true'
    if args.includeallorigins:
        params['includeallorigins'] = 'true'
    if args.includearrivals:
        params['includearrivals'] = 'true'
    if args.includedeleted:
        params['includedeleted'] = args.includedeleted
    if args.includesuperseded:
        params['includesuperseded'] = 'true'
    if args.limit:
        params['limit'] = args.limit
    if args.maxdepth is not None:
        params['maxdepth'] = args.maxdepth
    if args.maxmagnitude is not None:
        params['maxmagnitude'] = args.maxmagnitude
    if args.mindepth is not None:
        params['mindepth'] = args.mindepth
    if args.minmagnitude is not None:
        params['minmagnitude'] = args.minmagnitude
    if args.offset:
        params['offset'] = args.offset
    if args.orderby:
        params['orderby'] = args.orderby

    # Extensions
    if args.alertlevel:
        params['alertlevel'] = args.alertlevel
    if args.callback:
        params['callback'] = args.callback
    if args.eventtype:
        params['eventtype'] = args.eventtype
    if args.jsonerror:
        params['jsonerror'] = 'true'
    if args.kmlanimated:
        params['kmlanimated'] = 'true'
    if args.kmlcolorby:
        params['kmlcolorby'] = args.kmlcolorby
    if args.maxcdi is not None:
        params['maxcdi'] = args.maxcdi
    if args.maxgap is not None:
        params['maxgap'] = args.maxgap
    if args.maxmmi is not None:
        params['maxmmi'] = args.maxmmi
    if args.maxsig is not None:
        params['maxsig'] = args.maxsig
    if args.mincdi is not None:
        params['mincdi'] = args.mincdi
    if args.minfelt is not None:
        params['minfelt'] = args.minfelt
    if args.mingap is not None:
        params['mingap'] = args.mingap
    if args.minsig is not None:
        params['minsig'] = args.minsig
    if args.nodata:
        params['nodata'] = args.nodata
    if args.producttype:
        params['producttype'] = args.producttype
    if args.productcode:
        params['productcode'] = args.productcode
    if args.reviewstatus:
        params['reviewstatus'] = args.reviewstatus

    return params