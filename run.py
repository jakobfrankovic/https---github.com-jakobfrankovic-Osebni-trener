import naredi_bazo
import spletni_vmesnik

vnos = input('Želite pripraviti in napolniti bazo? (da/ne):')

if vnos.lower() == 'da':
    naredi_bazo.pripravi_in_napolni_bazo()


spletni_vmesnik.run_bottle()