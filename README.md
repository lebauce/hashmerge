hashmerge: a Python library to merge deep hashes
================================================

hashmerge is a port of the excellent Perl module [Hash::Merge](http://search.cpan.org/~rehsack/Hash-Merge/)
written by Jens Rehsack.

It merges two arbitrarily deep hashes into a single hash. That
is, at any level, it will add non-conflicting key-value pairs from one
hash to the other, and follows a set of specific rules when there are key
value conflicts (as outlined below).  The hash is followed recursively,
so that deeply nested hashes that are at the same level will be merged 
when the parent hashes are merged. Please note that self-referencing
hashes, or recursive references, are not handled well by this method.

Values in hashes are considered to be either lists or tuples (`ARRAY`),
dictionaries (`HASH`), or otherwise are treated as `SCALAR`s. By default,
the data passed to the merge function will be cloned using the `copy.deepcopy`
method; however, if necessary, this behavior can be changed to use as many of
the original values as possible, using `set_clone_behavior`.

Because there are a number of possible ways that one may want to merge
values when keys are conflicting, hashmerge provides several preset
methods for your convenience, as well as a way to define you own.  
These are (currently):

## Usage

```
    import hashmerge
    merger = hashmerge.HashMerge()
    print merger.merge({'d': 123, 'l': [1]}, {'e': 456, 'l': [2]})

    merger2 = hashmerge.HashMerge(hashmerge.RIGHT_PRECEDENT)
    print merger2.merge({'d': 123, 'l': [1]}, {'e': 456, 'l': [2]})
```

## Left Precedence

This is the default behavior.

The values buried in the left hash will never
be lost; any values that can be added from the right hash will be
attempted.

## Right Precedence

Same as Left Precedence, but with the right
hash values never being lost

## Storage Precedence

If conflicting keys have two different
storage mediums, the 'bigger' medium will win; arrays are preferred over
scalars, hashes over either.  The other medium will try to be fitted in
the other, but if this isn't possible, the data is dropped.

## Retainment Precedence

No data will be lost; scalars will be joined
with arrays, and scalars and arrays will be 'hashified' to fit them into
a hash.

## Notes

Now you can safely abandon Perl.
