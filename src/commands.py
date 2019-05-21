
import inspect, sys, click, json

from models.image import Image
from descriptors import *

from functions import get_commands, bold

from log import logger
import logging as log

@click.group()
def cli():
    '''
    Allows you to call the application features using a shell interface
    '''

@cli.command('describe', short_help='Describe the scene based on two images')
@click.option('--reference', default='reference.png', help='Image containing only the reference object')
@click.option('--relative', default='relative.png', help='Image containing only the relative object')
@click.option('--cardinal', default=16, help='Sets the number of directions used to compute the histograms')
@click.option('--variance', default=30, help='Shape the gaussian mask applied on the computed histograms')
@click.option('--resize', default=1.0, help='Resize images before processing')
@click.option('--descriptor', default='AngularPresenceDescriptor', help='Sets the descriptor used')
@click.option('--rotate', default=0, help='Rotate the relative image in degrees')
@click.option('--output', default=None, help='Writes result in a file')
def describe(reference, relative, cardinal, variance, resize, descriptor, rotate, output):
    try:

        logger.debug('Loading reference image {}...'.format(bold(reference)))
        
        reference = Image(reference) \
            .resize(resize)

        logger.info('OK')
        logger.debug('Loading relative image {}...'.format(bold(relative)))
        
        relative = Image(relative) \
            .resize(resize) \
            .rotate(rotate)

        logger.info('OK')
        logger.debug('Merging images...')
        
        image = reference.merge(relative)

        logger.info('OK')
        
        klass = getattr(sys.modules['descriptors'], descriptor)
        descriptor = klass(reference, relative, cardinal, variance)

        logger.debug('Computing histogram with {}...'.format(bold(descriptor)))
        
        descriptor.compute_histogram()

        logger.info('OK')
        logger.debug('Describing scene...')
        
        desc = descriptor.describe()

        logger.info('OK')
        logger.success(json.dumps(desc, indent=4))
        logger.debug('Interpretting description...')
        
        txt = descriptor.interpret()

        refname = reference.fname
        relname = relative.fname
        refname = refname[refname.rfind('/')+1:]
        relname = relname[relname.rfind('/')+1:]

        logger.success('{} is {} {}'.format(refname, txt, relname))

        if output is not None:
            with open(output, 'w+') as f:
                f.write(json.dumps({
                    'histogram': descriptor.histogram.values,
                    'description': desc,
                    'parameters': {
                        'reference': str(reference),
                        'relative': str(relative),
                        'cardinal': cardinal,
                        'variance': variance,
                        'resize': resize,
                        'descriptor': str(descriptor),
                        'rotate': rotate
                    },
                    'interpretation': '{} is {} {}'.format(refname, txt, relname)
                }, indent=4))
    except Exception as e:
        logger.critical('ERROR: {}'.format(str(e)))