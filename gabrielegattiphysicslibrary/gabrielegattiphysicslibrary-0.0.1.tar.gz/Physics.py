#Created by me, Gabriele Gatti, hope you like it




#Earth Gravity constant in m/(s^2)
gravity = 9.81

#Light speed on void in meters per sec.
light = 299792452

#Distance Moon-Earth in meters
ME = 3.84*10**9

#Speed of sound on air in meters per sec.
sound = 340

#Astronomical Unit in meters
AU = 1.49*10**11

#Parsec in meters
parsec = 3.08*10**16

#Earth Mass in kilograms
earthMass = 5.98*10**24

#Sun Mass in kilograms
sunMass = 1.98*10**30

#Moon Mass in kilograms
moonMass = 7.342*10**22

#Earth Radius in meters
earthRadius = 6378*10**3

#Sun Radius in meters
sunRadius = 69634*10**4

#Moon Radius in meters
moonRadius = 1731*10**3

#Universal Gravity Constant in [(Newton * meters^2) / (kilograms^2)]
G = 6.67*10**(-11)

#Light year in meters
lightYear = 9.46*10**15

#Proton Mass in kilograms
massProt = 1.672*10**(-27)

#Electron Mass in kilograms
massElect = 9.109*10**(-31)

#Neutron Mass in kilograms
massNeut = 1.674*10**(-27)

#Absolute Zero in Celsius Deg
absZero = -273

#Avogadro Constant (with grams) in molecules per mole
avogadro = 6.022*10**23

#Ideal Gasses Constant in [(Joule) / (Mole × Kelvin Deg.)]
R = 8.316

#Thermal Expansion Coefficient 1/273 <=> 0.036
thermExpansCoeff = 1/273

#Planck Constant in [(meters^2 × kilograms) / (seconds)]
planck = 6.626*10**(-34)

#Stefan-Boltzmann Constant in [Watt/(meters^2 * Kelvin^4)]
stefBoltz = 5.67*10**(-8)

#Coulomb constant in [Newton × (meters^2) / (Coulomb^2)]
coulomb = 8.988*10**9

#Dielectric constant on void in [Faraday/meters]
dielectric = 8.854*10**(-12)

#Electron Volt in Joule
eV = 1.602*10**(-19)

#Silver resistivity
silverResistivity = 1.6*10**(-8)

#Copper resistivity
copperResistivity = 1.7*10**(-8)

#Iron resistivity 
ironResistivity = 1.3*10**(-7)

#Steel resistivity
steelResistivity = 1.8*10**(-7)

#Proportionality constant in [Newton/(Amprere**2)]
proportionConst = 2.7*10**(-7)

#Weber in [Maxwell]
weber = 10**8

#Tesla in [Gauss]
tesla = 10**6

#Atomic Mass Unit in kilograms
atomMassUnit = 1.66043*10**(-27)

#Air Density in [kilograms/(meters**3)]
airDensity = 1.29

#Water Density in [kilograms/(meters**3)]
waterDensity = 10**3

#Atmosphere in Pascal
atm = 1.013*10**5

#Angstrom in meters
angstrom = 10**(-19)

#Water viscosity at 0 Celsius deg, in [pascal*seconds]
waterViscosityDeg0 = 1.8*10**(-3)

#Water viscosity at 20 Celsius deg, in [pascal*seconds]
waterViscosityDeg20 = 10**(-3)

#Copper conducibility in [Watt/(meters*Kelvin)]
copperConducibil = 384

#Gold conducibility in [Watt/(meters*Kelvin)]
goldConducibil = 300

#Iron conducibility in [Watt/(meters*Kelvin)]
ironConducibil = 70

#Dry Air conducibility in [Watt/(meters*Kelvin)]
airConducibil = 0.02

#Carbon Emissivity
carbonEmissivity = 0.92

#Iron Emissivity
ironEmissivity = 0.40

#Copper Emissivity
copperEmissivity = 0.30

#Silver Emissivity
silverEmissivity = 0.05

#Force formula
def force(mass,acceleration):
    return (mass*acceleration)

#Distance formula
def distance(speed,time):
    return (speed*time)

#Speed formula
def speed(distance,time):
    return (distance/time)

#Time formula
def time(distance,speed):
    return (distance*speed)

#Work formula
def work(force,distance):
    return (force*distance)

#Acceleration formula
def acceleration(force,mass):
    return (force/mass)

#Density formula
def density(weight,volume):
    return (weight/volume)

#Intensity formula
def intensity(power,area):
    return (power/area)

#Potential Energy formula
def potentialEner(mass,acceleration,height):
    return (mass*acceleration*height)

#Kinetic Energy formula
def kineticEner(mass,speed):
    return ((1/2)*mass*(speed**2))

#Mechanic Energy formula
def mechanicalEner(potential,kinetic):
    return (potential+kinetic)

#Momentum formula
def momentum(mass,speed):
    return (mass*speed)

#Power formula
def power(work,time):
    return (work/time)

#Potential Gravitational Energy
def potGravEner(mass,height):
    return (mass*grav*height)

#Potential Elastic Energy
def potentElasticEnerg(elasticConstant,distance):
    return ((1/2)*elasticConstant*(distance**2))

#Poiseuille law 
def lawPoiseuille(tubeRadius,pressureVariation,fluidViscosity,tubeLength):
    return ((3.1416*(radius**4)*pressureVariation)/(8*fluidViscosity*tubeLength))

#Stokes law 
def lawStokes(fluidViscosity,radius,speed):
    return ((-6)*3.1416*fluidViscosity,radius*speed)

#Universal Gravitational Law (Gravitational Attraction Law)
def attractGrav(mass1,mass2,distance):
    return ((G*mass1*mass2)/(distance**2))

#Gravitational Field from a point-like material
def gravField(mass,distance):
    return ((G*mass)/(distance**2))

#Potential Gravitatonal Energy of an isolated system composed by two point-like materials, each with specific mass, at a specific distance separating them
def potentGravEnerv2(mass1,mass2,distance):
    return (((-G)*mass1*mass2)/(radius))

#Escape Speed
def escapeSpeed(mass,radius):
    return (sqrt((G*mass)/(radius)))

#Gay-Lussac first law  (Volume variation)
def lawLussac1(volume,celsiusDegTemperature):
    return (volume*(1+(1/273)*(celsiusDegTemperature)))

#Gay-Lussac second law (Pressure Variation)
def lawLussac2(pressure,celsiusDegTemperature):
    return (pressure*(1+(1/273)*(celsiusDegTemperaure)))

#Fourier Law (of conduction)
def lawFourier(termicConducibility,area,kelvinHeatVariation,time,width):
    return ((termicConducibility*area*kelvinHeatVariation*time)/(width))

#Irradied Heat 
def irradiedHeat(emissivity,area,kelvinCorpTemperature,kelvinEnviromentTemperature,time):
    return (emissivity*stefBoltz*area*(kelvinCorpTemperature-kelvinEnviromentTemperature)*time)

#Doppler effect (when listener get closer to the sound source) 
def dopplerA(speed,frequence):
    return ((1+(speed/340))*frequence)

#Doppler effect (when listener get far away from sound source)
def dopplerB(speed,frequence):
    return  ((1-(speed/340))*frequence)

#Coulomb law formula
def lawCoulomb(charge1,charge2,distance):
    return (coulomb*(((charge1*charge2)**2)**(0.5))/(distance**2))

#Gauss theorem, Flux of electric field
def gaussFlux(charge):
    return (charge/dielectric)

#Electric Potential Energy on electric Field formula from a point-like charge
def U(charge1,charge2,distance):
    return ((charge1*charge2)/(4*3.1416*dielectric*distance))

#Electric Potential Difference between two point from the charge position
def electPotentDiff(charge,distance1,distance2):
    return ((charge/(4*3.1416*dielectric))*((1/distance1)-(1/distance2)))

#Capacity of a conducer
def capacity(charge,potential):
    return (charge/potential)

#Density of energy of Electric Field
def energyDens(electricFieldModule):
    return ((1/2)*dielectric*(electricFieldmodule**2))

#First Ohm law
def lawOhm1(resistance,currentIntensity):
    return (resistance*currentIntensity)

#Second Ohm law
def lawOhm2(resistivity,length,area):
    return (resistivity*lenght/area)

#Joule law
def lawJoule(resistance,currentIntensity):
    return (resistance*(currentIntensity**2))

#Magnetic Induction module
def B(magneticForce,currentIntensity,length):
    return (magneticForce/(currentIntensity*length))

#Ampere law
def lawAmpere(currentInt1,currentInt2,length,distance):
    return ((proportCon*currentInt1*currentInt2*length)/distance)

#Energetic Density Mean 
def energDensM(wavingElectricFieldWidth):
    return ((1/2)*dielectric*(wavingElectricFieldWidth**2))

#Relativistic time (Expansion of times)
def relativTime(travelerTime,speed):
    return [travelerTime/((1-((speed**2)/(light**2)))**(0.5))]

#Lorentz factor
def lorentzFact(speed):
    return [1/((1-((speed**2)/(light**2)))**(0.5))]

#Relativistic distance (Compression of distances)
def relativDist(nonTravelerDistance,speed):
    return (((1-(speed**2/light**2))**(0.5))*nonTravelerDistance)

#Relativistic Mass (Increment of Mass)
def relativMass(travelerMass,speed):
    return  [travelerMass/((1-((speed**2)/(light**2)))**(0.5))]

#Relativistic Momentum (Increment of Momentum)
def relativMomen(travelerMomentum,speed):
    return   [(travelerMomentum*speed)/((1-((speed**2)/(light**2)))**(0.5))]

#Relative Energy
def relativEnerg(travelerEnergy,speed):
    return [(travelerEnergy*(light**2))/((1-((speed**2)/(light**2)))**(0.5))]

#Quantic energy
def quanticEn(frequence):
    return (planck*frequence)

#Created by me, Gabriele Gatti, hope you like it
