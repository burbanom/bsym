import numpy as np

class SymmetryOperation:
    """
    `SymmetryOperation` class.
    """

    def __init__( self, matrix, label=None ):
        """
        Initialise a `SymmetryOperation` object

        Args:
            matrix (numpy.matrix|numpy.ndarray|list): 1D vector as either a
            `numpy.matrix`, `numpy.ndarray`, or `list` containing the site mappings
            for this symmetry operation.
            label (default=None) (str): optional string label for this `SymmetryOperation`
            object. Useful for the `SpaceGroup.by_label()` method.
        Raises:
            TypeError: if matrix is not `numpy.matrix`, `numpy.ndarray`, or `list`.

        Returns:
            self
        """
        if isinstance( matrix, np.matrix ):
            self.matrix = matrix
        elif isinstance( matrix, np.ndarray ):
            self.matrix = np.matrix( matrix )
        elif isinstance( matrix, list):
            self.matrix = np.matrix( matrix )
        else:
            raise TypeError
        self.label = label

    def __mul__( self, other ):
        """
        Multiply this `SymmetryOperation` matrix with another `SymmetryOperation`.

        Args:
            other (SymmetryOperation, matrix): the other symmetry operation or matrix
            for the matrix multiplication self * other.

        Returns:
            (SymmetryOperation): a new `SymmetryOperation` instance with the resultant matrix.
        """
        if isinstance( other, SymmetryOperation ):
            return( SymmetryOperation( self.matrix * other.matrix ) )
        else:
            return( SymmetryOperation( self.matrix * other ) )

    def invert( self ):
        """
        Invert this `SymmetryOperation` object.

        Args:
            None
 
        Returns:
            A new `SymmetryOperation` object corresponding to the inverse matrix operation.
        """
        return SymmetryOperation( np.linalg.inv( self.matrix ).astype( int ) )

    @classmethod
    def from_vector( cls, vector, count_from_zero = False ):
        """
        Initialise a SymmetryOperation object from a vector of site mappings.

        Args:
            vector (list): vector of integers defining a symmetry operation mapping.
            count_from_zero (default = False) (bool): set to True if the site index counts from zero.
   
        Returns:
            a new SymmetryOperation object
        """
        if not count_from_zero:
            vector = [ x - 1 for x in vector ]
        dim = len( vector )
        new_symmetry_operation = cls( np.zeros( ( dim, dim ), dtype=int ) )
        for index, element in enumerate( vector ):
            new_symmetry_operation.matrix[ index, element ] = 1
        return new_symmetry_operation

    def similarity_transform( self, s ):
        """
        Generate the SymmetryOperation produced by a similarity transform S^{-1}.M.S

        Args:
            s: the symmetry operation or matrix S.

        Returns:
            the SymmetryOperation produced by the similarity transform
        """
        return( s.invert() * self * s )

    def operate_on( self, configuration ):
        """
        Return the site occupation vector generated by appliying this symmetry operation

        Args:
            configuration (Configuration): the configuration / occupation vector to operate on

        Returns:
            the new configuration obtained by operating on configuration with this symmetry operation. 
        """
        # returns the site occupation vector generated by applying this symmetry operation
        from bsym import configuration as conf
        new_configuration = conf.Configuration( ( self.matrix * configuration ).tolist() )
        return( new_configuration )

    def character( self ):
        """
        Return the character of this symmetry operation (the trace of `self.matrix`).

        Args:
            none

        Returns:
            np.trace( self.matrix )
        """
        return np.trace( self.matrix )

    def as_vector( self, count_from_zero = False ):
        """
        Return a vector representation of this symmetry operation

        Args:
            count_from_zero (default = False) (bool): set to True if the vector representation counts from zero
      
        Returns:
            a vector representation of this symmetry operation (as a list)
        """
        offset = 0 if count_from_zero else 1
        return( [ row.index( 1 ) + offset for row in self.matrix.tolist() ] )

    def set_label( self, label ):
        """
        Set the label for this symmetry operation.
  
        Args:
            label: label to set for this symmetry operation
        Returns:
            self 
        """
        self.label = label
        return( self )

    def pprint( self ):
        """
        Pretty print for this symmetry operation

        Args:
            None
        Returns:
            None
        """
        label = self.label if self.label else '---'
        print( label + ' : ' + ' '.join( [ str(e) for e in self.as_vector() ] ) )
        
    def __repr__( self ):
        label = self.label if self.label else '---'
        return 'SymmetryOperation\nlabel(' + label + ")\n" + self.matrix.__repr__()

    def _repr_html( self ):
        return self.matrix._repr_html_()
    
        
