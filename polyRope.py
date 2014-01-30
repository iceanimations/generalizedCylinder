import pymel.core as pc
from generalizedCylinder import generalizedCylinder, _pattern

def polyRope(curve, name='polyRope1',
        midSamplesPerLength=2.,midTwistRate=2., midWidth=0.75,
        midRebuildSpansMult = 4, midAdjustUVs = True, midCloseEnds=True,
        numSideCyls = 4, showMidCylinder=1,
        sideSamplesPerLength=2., sideTwistRate=1., sideWidth=0.5,
        sideRebuildSpansMult = 4, sideAdjustUVs = True, sideCloseEnds=True,
        sideTubeSections = 4):
    ''' create a polyRope with one mid cylinder and some sideCylinders '''
    maingrp = pc.createNode('transform', n=name)
    maingrp.addAttr("midWidth", at="float", dv=midWidth, k=True)
    maingrp.addAttr("midTwistRate", at="float", dv=midTwistRate, k=True)
    maingrp.addAttr("sideWidth", at="float", dv=sideWidth, k=True)
    maingrp.addAttr("sideTwistRate", at="float", dv=sideTwistRate, k=True)
    maingrp.addAttr("showMidCylinder", at="bool", dv=showMidCylinder, k=True)

    match = _pattern.match(str(maingrp))
    if not match:
        num = ""
        name = name.split("|")[-1]
    else:
        name = match.group(1).split("|")[-1]
        num = match.group(2)

    if numSideCyls < 3:
        numSideCyls = 3

    # create mid cylinder
    midCyl = generalizedCylinder(curve, name = name + num + 'MidCylinder',
            parent = maingrp, 
            samplesPerLength=midSamplesPerLength, tubeSections=numSideCyls,
            twistRate=midTwistRate, brushWidth=midWidth,
            rebuildSpansMult=midRebuildSpansMult, adjustUVs=midAdjustUVs,
            closeEnds=midCloseEnds)
    maingrp.midWidth >> midCyl.width
    maingrp.midTwistRate >> midCyl.twistRate
    maingrp.showMidCylinder >> midCyl.v
    midCylShape = midCyl.getShape(type='mesh')

    curves_grp = pc.createNode('transform',n=name+num+'CurvesGrp', p=maingrp)
    side_cyl_grp = pc.createNode('transform',n=name+num+'SideCylindersGrp', p=maingrp)

    sideCyls = []
    # funk you ... creating all the side cylinders
    for scn in range(numSideCyls):
        pc.select(midCylShape, r=True)
        edgeLoop = pc.polySelect(q=1, el=2*numSideCyls+scn)
        edgeLoop = sorted(edgeLoop)
        # make a curve from edgeloop and create a cyl around it
        cfme = pc.createNode('curveFromMeshEdge', 
                n=name+num+"CurveFromMeshEdge1")
        for i, e in enumerate(edgeLoop):
            cfme.ei[i].set(e)
        elc = pc.createNode('transform', n=name+num+'EdgeLoopCurve'+str(scn),
                p=curves_grp)
        elcShape = pc.createNode('nurbsCurve', 
                n=name+num+'EdgeLoopCurveShape'+str(scn), p=elc)
        dc = pc.createNode('detachCurve', n=name+num+'EdgeLoopDetachCurve1')
        dc.p[0].set(len(edgeLoop)-3)
        dc.k[0].set(1)
        dc.k[1].set(0)
        midCylShape.outMesh >> cfme.inputMesh
        cfme.oc >> dc.ic
        dc.oc[0] >> elcShape.create
        sc = generalizedCylinder(elcShape, name=name+num+'SideCylinder1',
                parent=side_cyl_grp, samplesPerLength=sideSamplesPerLength,
                tubeSections=sideTubeSections, twistRate=sideTwistRate,
                brushWidth=sideWidth, rebuildSpansMult=sideRebuildSpansMult,
                adjustUVs=sideAdjustUVs, closeEnds=sideCloseEnds)
        maingrp.sideWidth >> sc.width
        maingrp.sideTwistRate >> sc.twistRate
        sideCyls.append(sc)

def _main_():
    """test the polyRopeFucntion on all curves in a maya scene
    :returns: None
    """
    ncs = pc.ls(type='nurbsCurve', sl=1)
    mpb = pc.ui.MainProgressBar(0, len(ncs))
    mpb.beginProgress()
    for i in ncs:
        if mpb.getIsCancelled(): break
        polyRope(i)
        if mpb.getIsCancelled(): break
        mpb.step()
    mpb.endProgress()

if __name__ == '__main__':
    _main_()
